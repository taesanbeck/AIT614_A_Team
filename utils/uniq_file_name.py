# uniq_file_name.py
import os

# this is for the page 1 auto converting of temp nitf file names so the users most recent upload is the file being used
def generate_unique_filename(base_path, base_filename):
    counter = 1
    while os.path.exists(os.path.join(base_path, base_filename + str(counter) + ".jpg")):
        counter += 1
    return os.path.join(base_path, base_filename + str(counter) + ".jpg")