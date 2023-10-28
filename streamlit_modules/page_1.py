from objects.yolo8 import output_class_list
from objects.yolo8 import output_class_list_w_meta
from objects.yolo8 import run_yolo8
from PIL import Image
import streamlit as st
import io
import os
from objects.delete_imgs import delayed_delete
from database.db import David_db as db
from utils.handle_img_upload import handle_uploaded_image


def show_page(selected_cv_model, selected_nlp_model):

    st.title('Predict Objects')

    st.header('Upload an image:')
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "nitf", "ntf"])

    png_file = None  # Initialize the variable here
    image_input = None  # Initialize image_input here

    # handle uploaded image, output nitf metadat and jpg image
    # Only proceed if an image has been uploaded
    if uploaded_file is not None:
        # handle uploaded image, output nitf metadat and jpg image
        png_file, extracted_nitf_metadata = handle_uploaded_image(uploaded_file)

    st.header('Confidence Level:')
    confidence_level = st.slider('Adjust the confidence level', min_value=0.0, max_value=1.0, value=0.1)

    st.header('Bounding Boxes:')
    bounding_box_option = st.radio('Would you like bounding boxes displayed?', ('Yes', 'No'))

    if png_file is not None and st.button('Run Models'):
        png_file = open(f'{png_file}', 'rb') # rb stands for read binary mode
        image_data = png_file.read()
        
        image_input = Image.open(io.BytesIO(image_data))
        
        # Resize image while maintaining aspect ratio
        base_width = 640
        w_percent = base_width / float(image_input.size[0])
        h_size = int(float(image_input.size[1]) * float(w_percent))
        image_input = image_input.resize((base_width, h_size), Image.ANTIALIAS)

        image_name = uploaded_file.name

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


    # delete images on a timer
    delayed_delete('../AIT614_A_TEAM/objects/saved_img', 3*60)

    try:
        labels = None
        location_labels = None

        if image_input is not None and          selected_cv_model == 'YOLOV8':
            raw_results, image_output = run_yolo8(image_input, image_name, bounding_box_option, confidence_level)

            # Update location_labels here
            location_labels = raw_results

            if not location_labels or len(location_labels) == 0:
                st.error('No objects detected in the uploaded image.')

            else:
                
                #Split lower page into 2 columns
                col1, col2 = st.columns(2)

                with col1:
                                        
                    # to get the nitf metadata
                    import pandas as pd
                    all_data = [extracted_nitf_metadata] + location_labels
                    df = pd.DataFrame(all_data)

                    st.write(df)

                    options = list(df['class_name'])
                    selected = st.multiselect("Remove Predictions:", options)
                    df = df[~df['class_name'].isin(selected)]

                    if st.button('Database'):
                        db.insert_metadata(extracted_nitf_metadata, df.to_dict(orient='records'), image_data)
                        st.success("Data added to the database!")
                        
                with col2:
                    docs = db.db_instance.col.find({})
                    all_data = list(docs)
                    db_df = pd.DataFrame(all_data)
                    st.write(db_df)

    except Exception as e:
        st.error(f'Error: {e}')