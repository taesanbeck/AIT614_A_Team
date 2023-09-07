from objects.yolo8 import output_class_list, output_class_list_w_meta, run_yolo8
from objects.yolo3 import run_yolo3
from PIL import Image
import streamlit as st
from tts.texttospeech import texttospeech  
from actions.yolo_act import run_yolo_act, output_class_list_w_action
from nlp.t5_coco import run_t5
from nlp.t5_common_gen import run_t5_common_gen
from scenes.densenet import run_densenet  # Assuming this is where your run_densenet function is located
import io
import os
from nlp.preProcess import preprocess_labels
from ocr.ocr import run_ocr
import cv2
from objects.delete_imgs import delayed_delete
from PIL import Image, ExifTags

def show_page(selected_cv_model, selected_nlp_model):

    st.title('Model Testing')

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
        delayed_delete('../AThousandWords/objects/saved_img', 3*60)


        try:
            labels = None
            location_labels = None
            if selected_cv_model == 'YOLOV8':
                raw_results = run_yolo8(image_input, image_name, bounding_box_option, confidence_level)
                if 'person' in output_class_list(raw_results):
                    raw_results = run_yolo_act(image_input,confidence_level,raw_results)
                labels = output_class_list_w_action(raw_results)
                location_labels = output_class_list_w_meta(raw_results)  # Extract location labels from the raw results

                # run scene recognition, output updated labels
                labels, raw_results = run_densenet(raw_results, labels, image_input)
                
                if not labels:
                    st.error('No objects detected in the uploaded image.')
                    # Generate a default message
                    default_message = "No objects detected in the image."
                    texttospeech(default_message)  # Convert default_message to audio
                    
                    audio_file = open("output.mp3", "rb")
                    st.audio(audio_file.read(), format='audio/mp3')  # Play audio
                    audio_file.close()
                else:
                    # Create two columns
                    col1, col2 = st.columns(2)

                    # Column 1 - Human Readable Caption/Preprocessed
                    with col1:
                        # Preprocess labels here
                        preprocessed_labels = preprocess_labels(labels)
                        
                        if preprocessed_labels:
                            if selected_nlp_model == 'T5_Common_Gen':
                                caption = run_t5_common_gen(preprocessed_labels) # Capture the returned caption 
                            elif selected_nlp_model == 'T5_coco(BabyT5)':
                                caption = run_t5(preprocessed_labels) # Capture the returned caption 
                            

                        objects = [label for label in labels if 'scene' not in label]
                        if objects:
                            st.header('Objects/Actions:')
                            st.write(', '.join(objects))
                        
                        actions = [label for label in labels if 'action' in label]
                        if actions:
                            st.header('Actions:')
                            st.write(', '.join(actions))

                        scenes = [str(label['scene']) for label in raw_results if 'scene' in label]
                        if scenes:
                            st.header('Scenes:')
                            st.write(', '.join(scenes))
                    
                    # Column 2 - Location data/OCR when I get it
                    with col2:
                        location_string = ''
                        if location_labels:
                            st.header('Location data:')
                            st.write(location_labels)

                            # Convert location_labels to string
                            location_string = ', '.join(location_labels)
                        
                        #Get OCR predictions here
                        st.header('OCR Results:')
                        predicted_texts, image_with_boxes = run_ocr(image_data, bounding_box_option)
                  
                        st.image(image_with_boxes, use_column_width=False, width=200)  # Display the image

                        if predicted_texts:
                            # Combine words into a single string
                            ocr_statement = ' '.join(predicted_texts)
                            # add pauses in the text output
                            ocr_tts_statement = ocr_statement.replace(' ', '... ')
                            st.write(ocr_statement)
                            tts_statement = 'The image contains the following text: ' + ocr_tts_statement  # This line is for the TTS function
                        else:
                            ocr_statement = "No text was detected in the image."
                            st.write(ocr_statement)
                            tts_statement = 'No text was detected in the image. ' # This line is for the TTS function

                # Combine caption, location, and OCR data
                combined_text = '. '.join([caption, location_string, tts_statement])
                print(combined_text)

                texttospeech(combined_text)  # Pass combined_text to TTS function

                audio_file = open("output.mp3", "rb")
                st.audio(audio_file.read(), format='audio/mp3')  # Play audio
                audio_file.close()
                
            elif selected_cv_model == 'YOLOV3':
                labels = run_yolo3(image_input, image_name, confidence_level, bounding_box_option)
                labels = labels.split()

                if not labels:
                    st.error('No objects detected in the uploaded image.')
                    # Generate a default message
                    default_message = "No objects detected in the image."
                    texttospeech(default_message)  # Convert default_message to audio
                                
                    audio_file = open("output.mp3", "rb")
                    st.audio(audio_file.read(), format='audio/mp3')  # Play audio
                    audio_file.close()
                else:
                    if selected_nlp_model == 'T5_Common_Gen': 
                        caption = run_t5_common_gen(labels) # Capture the returned caption
                    elif selected_nlp_model == 'T5_coco(BabyT5)': 
                        caption = run_t5(labels) # Capture the returned caption
                    
                    # convert the captions to speech
                    texttospeech(caption)
                    
                    audio_file = open("output.mp3", "rb")
                    st.audio(audio_file.read(), format='audio/mp3')  # Play audio
                    audio_file.close()


        except Exception as e:
            st.error(f'Error: {e}')


