# main.py
from streamlit_modules import default
from streamlit_modules import sidebar
from streamlit_modules import page_1
from streamlit_modules import page_2
from streamlit_modules import page_3

# Retrieve AWS credentials from environment variables
#aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
#aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# If you want to do this it should be happening here, not in random modules - AV

def main():
    # Set up page layout and theme
    default.default_page_config()

    # Show sidebar and get current page
    page, selected_cv_model = sidebar.show_sidebar(['Predict and Database', 'Map', 'About'])

    # Display the selected page
    if page == "Predict and Database":
        page_1.show_page(selected_cv_model)  
    elif page == "Map":
        # need to add model selection for the Map page as well
        page_2.show_page()
    elif page == "About":
        page_3.show_page()


if __name__ == "__main__":
    main()




