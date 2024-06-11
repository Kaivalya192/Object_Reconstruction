import os
import shutil
from PIL import Image

# Define the source and destination paths
source_folder = 'input/rgb'
destination_folder = os.path.join('input/JPEGImages', 'video1')

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Function to convert PNG to JPG
def convert_png_to_jpg(source_path, destination_path):
    with Image.open(source_path) as img:
        rgb_img = img.convert('RGB')
        destination_path = destination_path.replace('.png', '.jpg')
        rgb_img.save(destination_path, 'JPEG')

# Copy the contents of the source folder to the destination folder
for item in os.listdir(source_folder):
    source_item = os.path.join(source_folder, item)
    destination_item = os.path.join(destination_folder, item)
    
    if os.path.isdir(source_item):
        shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
    else:
        if source_item.lower().endswith('.png'):
            convert_png_to_jpg(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)

print(f'Contents of {source_folder} copied to {destination_folder}, and PNG files converted to JPG')
