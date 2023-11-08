# handle_img_upload.py
import os
from objects.delete_imgs import delayed_delete
from utils.uniq_file_name import generate_unique_filename
from utils.nitf_to_png import nitf_to_png
from utils.extract_ntf_metadata import extract_nitf_metadata
from database.db import David_db as db

def handle_uploaded_image(uploaded_file):

    # grab image name
    image_name = uploaded_file.name
  
    # Define paths for saving files
    saved_dir_path = "AIT614_A_TEAM/objects/saved_img/"
    saved_file_path = os.path.join(saved_dir_path, image_name)
    
    # Ensure the directory exists
    if not os.path.exists(saved_dir_path):
        os.makedirs(saved_dir_path)
    
    # Save the uploaded file to the specified path
    with open(saved_file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    nitf_path = saved_file_path  # Now you have a proper path to the file

    # Convert the NITF to PNG using the provided Jupyter code
    png_file = nitf_to_png(nitf_path, image_name)
    
    # Get the absolute path of the png_file
    png_file = os.path.abspath(png_file)
    
    # Extract NITF metadata
    extracted_nitf_metadata = extract_nitf_metadata(nitf_path)
    
    # Schedule a delayed delete for both NITF and PNG files after processing
    delayed_delete(nitf_path, delay=3*60)  # delay in seconds
    delayed_delete(png_file, delay=3*60)

    return png_file, extracted_nitf_metadata 
