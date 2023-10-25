#page_1.py
from objects.yolo8 import output_class_list, output_class_list_w_meta, run_yolo8
from PIL import Image
import streamlit as st
import io
import os
import cv2
from objects.delete_imgs import delayed_delete
from PIL import Image, ExifTags

def show_page(selected_cv_model, selected_nlp_model):

    st.title('Predict Objects')

    st.header('Upload an image:')
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    st.header('Confidence Level:')
    confidence_level = st.slider('Adjust the confidence level', min_value=0.0, max_value=1.0, value=0.5)

    st.header('Bounding Boxes:')
    bounding_box_option = st.radio('Would you like bounding boxes displayed?', ('Yes', 'No'))

     # Add a button to run the model and generate a caption
    if st.button('Run Models'):
        if uploaded_file is not None:
            image_data = uploaded_file.read()
            image_input = Image.open(io.BytesIO(image_data))
            image_name = uploaded_file.name
        
            # Check if the image has EXIF(Orientation) data for iPhone rotation issue
            if hasattr(image_input, '_getexif'):
                exif_data = image_input._getexif()
                if exif_data:
                    # Get the orientation tag from the EXIF data
                    orientation_tag = ExifTags.TAGS.get('Orientation')
                    orientation = exif_data.get(orientation_tag)
                    
                    # Rotate the image based on its orientation
                    if orientation == 3:
                        image_input = image_input.rotate(180, expand=True)
                    elif orientation == 6:
                        image_input = image_input.rotate(270, expand=True)
                    elif orientation == 8:
                        image_input = image_input.rotate(90, expand=True)
        
        
        # delete all files in the `saved_img` directory every 3 minutes
        delayed_delete('../AIT614_A_TEAM/objects/saved_img', 3*60)

        try:
            labels = None
            location_labels = None
            if selected_cv_model == 'YOLOV8':
                raw_results = run_yolo8(image_input, image_name, bounding_box_option, confidence_level)

                location_labels = output_class_list_w_meta(raw_results)  # Extract location labels from the raw results
                
                if not labels:
                    st.error('No objects detected in the uploaded image.')
                    # Generate a default message
                    default_message = "No objects detected in the image."
                else:
                    # Create two columns (View and Database)
                    col1, col2 = st.columns(2)


        except Exception as e:
            st.error(f'Error: {e}')


