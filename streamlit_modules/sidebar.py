# sidebar.py
import streamlit as st
from PIL import Image

def show_sidebar(page_options):  
    st.sidebar.image('streamlit_modules/media/gmu_image.png', output_format='auto',channels='RGB')
    st.sidebar.write('_____________________________________')
    st.sidebar.image('streamlit_modules/media/david.png', output_format='auto',channels='RGB')
    # Add navigation
    page = st.sidebar.selectbox("Go to", page_options, key="sidebar_selectbox")

    # Add a selectbox for CV model
    selected_cv_model = None
    if page == "Predict and Database":
        selected_cv_model = st.sidebar.selectbox('Select CV Model', ['YOLOV8', 'YOLOV8_xView'])
        
    # Add a button for running the application if 'About' page is selected
    if page == "Map":
        st.sidebar.button('Run Application')

    return page, selected_cv_model

    
