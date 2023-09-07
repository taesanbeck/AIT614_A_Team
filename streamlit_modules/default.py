# default.py
import streamlit as st

def default_page_config():
    # Set page layout to wide
    st.set_page_config(layout="wide")

    # Add CSS to set the theme to dark mode
    st.markdown(
        """
        <style>
        :root {
            --color-primary: #262730;
            --color-on-primary: #ffffff;
            --color-secondary: #0072B2;
            --color-on-secondary: #ffffff;
            --color-background: #1F1F1F;
            --color-on-background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )