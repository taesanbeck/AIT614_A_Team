# sidebar.py
import streamlit as st
from PIL import Image

def show_sidebar(page_options):  
    st.sidebar.image('streamlit_modules/media/gmu_image.png', output_format='auto',channels='RGB')
    st.sidebar.write('_____________________________________')
    st.sidebar.image('streamlit_modules/media/ida.png', output_format='auto',channels='RGB')
    # Add navigation
    page = st.sidebar.selectbox("Go to", page_options, key="sidebar_selectbox")

    # Add a selectbox for CV model
    selected_cv_model = None
    selected_nlp_model = None
    if page == "Model Testing":
        selected_cv_model = st.sidebar.selectbox('Select CV Model', ['YOLOV8', 'YOLOV3'])
        selected_nlp_model = st.sidebar.selectbox('Select NLP Model', ['T5_Common_Gen', 'T5_coco(BabyT5)']) 

    # Add a button for running the application if 'About' page is selected
    if page == "App":
        st.sidebar.button('Run Application')

    return page, selected_cv_model, selected_nlp_model


    
