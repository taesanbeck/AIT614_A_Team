import os
import threading

print(os.getcwd())

# Function to delete files at a specified path
def delete_files(path):
    # Check if the path is a directory
    if os.path.isdir(path):
        # Iterate over each file in the directory
        for filename in os.listdir(path):
            # Generate the full path for the file
            file_path = os.path.join(path, filename)
            try:
                # If the file_path is a file or a symbolic link, then delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # If the file_path is a directory, then remove it
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Note: This will only remove empty directories
            # If there's any issue during file deletion, catch the exception and print it
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    # If the path is a file, then delete it
    elif os.path.isfile(path) or os.path.islink(path):
        try:
            os.unlink(path)
        except Exception as e:
            print(f'Failed to delete {path}. Reason: {e}')


# Function to initiate delayed deletion of files
def delayed_delete(path, delay):
    # Schedule the delete_files function to run after `delay` seconds.
    threading.Timer(delay, periodic_delete, [path, delay]).start()

# Function to periodically delete files every `delay` seconds.
def periodic_delete(path, delay):
    # Delete the files at the path
    delete_files(path)
    # Schedule the next call for periodic_delete function after `delay` seconds.
    threading.Timer(delay, periodic_delete, [path, delay]).start()