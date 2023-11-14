from objects.yolo8 import output_class_list
from objects.yolo8 import output_class_list_w_meta
from objects.yolo8 import run_yolo8
from PIL import Image
import streamlit as st
import io
import os
from objects.delete_imgs import delayed_delete
from database.db import db_instance
from utils.handle_img_upload import handle_uploaded_image
import pandas as pd
from utils.pixel_to_geo import pixel_to_geo


@st.cache_data(experimental_allow_widgets=True)
def show_page(selected_cv_model):
    from database.db import db_instance
    import pandas as pd
    
    # Initialize combined_df in session state if it doesn't exist
    if 'combined_df' not in st.session_state:
        st.session_state['combined_df'] = pd.DataFrame()
        

    
    st.title('Predict Objects')

    st.header('Upload an image:')
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "nitf", "ntf"])

    # Initialize and cache image_input here
    image_input = None
    if 'image_input' not in st.session_state:
        st.session_state['image_input'] = None  
    
    # to  initialize and cache png file
    png_file = None
    if 'png_file' not in st.session_state: 
            st.session_state['png_file'] = None
            
    # handle uploaded image, output nitf metadat and png image
    # Only proceed if an image has been uploaded
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None
    if uploaded_file is not None:
        # handle uploaded image, output nitf metadat and jpg image
        png_file, extracted_nitf_metadata = handle_uploaded_image(uploaded_file)
        
        if png_file is not None:
            st.markdown("<h1 style='text-align: left; color: green;font-size: 20px;'>NTF image successfully converted to PNG!!</h1>", unsafe_allow_html=True)

    with st.form(key='model_selection_form'):
        st.header('Confidence Level:')
        confidence_level = st.slider('Adjust the confidence level', min_value=0.0, max_value=1.0, value=0.1)

        st.header('Bounding Boxes:')
        bounding_box_option = st.radio('Would you like bounding boxes displayed?', ('Yes', 'No'))
        submitted = st.form_submit_button('Run Models')


    import os

    # Streamlit app is run from the AIT614_A_TEAM directory
    # Get the current working directory
    current_working_directory = os.getcwd()

    # Construct the relative path to the saved images
    saved_images_directory = os.path.join(current_working_directory, 'objects', 'saved_img')

    # Relative path to Streamlit app
    if png_file is not None and submitted:
        # Assuming 'png_file' is the name of the file and not the full path
        full_file_path = os.path.join(saved_images_directory, png_file)

        with open(full_file_path, 'rb') as file:
            image_data = file.read()
        
        image_input = Image.open(io.BytesIO(image_data))
        
        # Resize image while maintaining aspect ratio
        base_width = 640
        w_percent = base_width / float(image_input.size[0])
        h_size = int(float(image_input.size[1]) * float(w_percent))
        image_input = image_input.resize((base_width, h_size), Image.ANTIALIAS)

        image_name = uploaded_file.name

        
        # This code to handle rotating images on phones
        #if hasattr(image_input, '_getexif'):
            #exif_data = image_input._getexif()
            #if exif_data:
                #orientation_tag = 274
                #orientation = exif_data.get(orientation_tag)
                #if orientation == 3:
                    #image_input = image_input.rotate(180, expand=True)
                #elif orientation == 6:
                    #image_input = image_input.rotate(270, expand=True)
                #elif orientation == 8:
                    #image_input = image_input.rotate(90, expand=True)
    
        
    delayed_delete('../AIT614_A_TEAM/objects/saved_img', 3*60)

    labels = None
    location_labels = None
    

    if image_input is not None and selected_cv_model == 'YOLOV8':
        raw_results, image_output = run_yolo8(image_input, image_name, bounding_box_option, confidence_level)

        if not raw_results or len(raw_results) == 0:
            st.error('No objects detected in the uploaded image.')
            
            
        
        # Split lower page into 2 columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Create DataFrame for predictions
            import pandas as pd
            predictions_df = pd.DataFrame(raw_results)
            
            # Create DataFrame for NITF metadata
            nitf_metadata_df = pd.DataFrame([extracted_nitf_metadata])

            # Replicate NITF metadata DataFrame for each prediction
            nitf_metadata_replicated = pd.concat([nitf_metadata_df] * len(predictions_df), ignore_index=True)
            
            # Concatenate predictions and NITF metadata side-by-side
            combined_df = pd.concat([predictions_df, nitf_metadata_replicated], axis=1)
            print("Debug combined_df after construction:")
            print(combined_df)


            # Convert pixel centroid to grids
            for i, row in combined_df.iterrows():
                centroid_pixel = row['centroid']  # Directly access the centroid without eval()
                
                if isinstance(centroid_pixel, str):  # Check if the centroid is a string, then evaluate
                    centroid_pixel = eval(centroid_pixel)
                    
                centroid_geo = pixel_to_geo(centroid_pixel, extracted_nitf_metadata['Geo Location'], image_input.size)
                
                # Assign the latitude and longitude of the geographic centroids to separate columns
                combined_df.at[i, 'centroid_latitude'] = centroid_geo[0]
                combined_df.at[i, 'centroid_longitude'] = centroid_geo[1]
                print("Debug combined_df after construction:")
                print(combined_df[['centroid_latitude', 'centroid_longitude']])

                
            # Columns to be dropped
            columns_to_drop = ['Mean GSD', 'Image Source', 'Std ID Location', 'Geo Location', 'Coord Representation', 'Image DateTime', 'centroid', 'id', 'xyxy']

            # Check and drop only the columns that exist in the DataFrame
            existing_columns_to_drop = [col for col in columns_to_drop if col in combined_df.columns]
            if existing_columns_to_drop:
                combined_df.drop(columns=existing_columns_to_drop, inplace=True, axis=1)
                
                # Store the resulting DataFrame in session state
                st.session_state['combined_df'] = combined_df
                
            else:
                st.error("Attempted to drop columns that do not exist in the DataFrame.")
    
    col1, col2 = st.columns([1,8])

    combined_df = st.session_state['combined_df']

    @st.cache_data
    def run_expensive_computation (combined_df):
        return combined_df

    # Use a form for the checkbox selections to avoid rerunning the app
    with col1:
        with st.form(key='selection_form'):
            # Create a dictionary to hold the checkbox states
            checkbox_states = {}

            # Create a checkbox for each row
            for index, row in combined_df.iterrows():
                # Define a unique key for each checkbox
                checkbox_key = f'select_{index}'

                # Create and store the checkbox in the session state
                checkbox_states[checkbox_key] = st.checkbox(
                    label=f'Select Row {index}',
                    value=st.session_state.get(checkbox_key, True),  # Default to True if not in session state
                    key=checkbox_key
                )
                print(checkbox_states)
                print(combined_df)

            # Place the submit button for the form
            submitted = st.form_submit_button('Database Predictions')
            
            
            # After constructing the combined_df, reset its index
            combined_df.reset_index(drop=True, inplace=True)

            # form submission logic
            if submitted and not st.session_state.get('data_processed', False):
                try:
                    # Collect selected indices based on checkbox states
                    selected_indices = [index for index, checked in enumerate(checkbox_states.values()) if checked]
                    print(f"Debug selected_indices: {selected_indices}")
                    
                    # Create the selected_df based on selected indices
                    selected_df = combined_df.loc[selected_indices]
                    print(f"Debug selected_df: {selected_df}")
                    
                    # Check for duplicates and insert the new data
                    # Run the insertion process and get the counts
                    inserted_count, duplicate_count = db_instance.check_and_insert_data(selected_df)
                    print(selected_df[['centroid_latitude', 'centroid_longitude']])

                    # Display the result to the user
                    st.success(f'Inserted {inserted_count} new entries. Skipped {duplicate_count} duplicates.')

                    # Update session state if needed
                    st.session_state['data_updated'] = True  # Example of updating the session state
                    
                    # After processing, set the session state to prevent reprocessing
                    st.session_state['data_processed'] = True

                except Exception as e:
                    st.error(f'An error occurred while processing the data: {str(e)}')

        
    with col2:
        st.write(combined_df)



    print(st.session_state)
                
    # Display the image outside the form to maintain its visibility
    if 'png_file' in st.session_state and st.session_state['png_file'] is not None:
        st.image(st.session_state['png_file'])
            
            
    # Now let's display the database contents in col2    
    import pandas as pd
    try:
        all_data = db_instance.fetch_all_data()
        if all_data:
            all_data_df = pd.DataFrame(all_data)
            # Convert ObjectId to string if needed
            all_data_df['_id'] = all_data_df['_id'].apply(lambda x: str(x))
            # Display the dataframe
            st.dataframe(all_data_df)
        else:
            st.write("No data available in the database.")
    except Exception as e:
        st.error(f"An error occurred while fetching data from the database: {e}")
            
        
        
                
            
        
            
        
        
        
                
        
