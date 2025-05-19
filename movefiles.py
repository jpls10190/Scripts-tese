import os
import shutil

# Specify the source directory and target directories
source_dir = os.getcwd()  # Current directory, change as needed
image_target_dir = 'images'  
txt_target_dir = 'labels'    

# Create target directories if they do not exist
os.makedirs(image_target_dir, exist_ok=True)
os.makedirs(txt_target_dir, exist_ok=True)

# List all files in the source directory
files_in_directory = os.listdir(source_dir)

# Define common image file extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

# Process each file
for file_name in files_in_directory:
    file_path = os.path.join(source_dir, file_name)
    
    if os.path.isfile(file_path):
        # Check file extension
        if any(file_name.lower().endswith(ext) for ext in image_extensions):
            # Move image file
            target_path = os.path.join(image_target_dir, file_name)
            shutil.move(file_path, target_path)
            print(f'Moved image file: {file_name} to {image_target_dir}')
        elif file_name.lower().endswith('.txt'):
            # Move text file
            target_path = os.path.join(txt_target_dir, file_name)
            shutil.move(file_path, target_path)
            print(f'Moved text file: {file_name} to {txt_target_dir}')

print('Files have been moved.')