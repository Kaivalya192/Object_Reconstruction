import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time
import shutil
from PIL import Image

base_dir = 'input'
sub_dirs = ['depth', 'rgb']

for sub_dir in sub_dirs:
    os.makedirs(os.path.join(base_dir, sub_dir), exist_ok=True)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()


clipping_distance_in_meters = 1  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

with open(os.path.join(base_dir, 'cam_K.txt'), 'w') as f:
    f.write("388.5970 0 325.1479\n")
    f.write("0 388.5970 240.6325\n")
    f.write("0 0 1\n")

print("Press Enter to start recording the sequence.")
while True:
    cv2.namedWindow('Press Enter to start recording', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Press Enter to start recording', np.zeros((100, 300), np.uint8))
    if cv2.waitKey(1) == 13:
        break
cv2.destroyAllWindows()

time.sleep(2)

print("Recording started. Press Enter to stop recording.")
frame_count = 0
recording = True

try:
    while recording:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        filename = f"{frame_count:08d}.png"
        rgb_filename = os.path.join(base_dir, 'rgb', filename)
        depth_filename = os.path.join(base_dir, 'depth', filename)

        cv2.imwrite(rgb_filename, color_image)
        cv2.imwrite(depth_filename, (depth_image * depth_scale * 1000).astype(np.uint16))

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        if cv2.waitKey(1) == 13:
            recording = False

        frame_count += 1
finally:
    pipeline.stop()
    cv2.destroyAllWindows()

source_folder = 'input/rgb'
destination_folder = os.path.join('input/JPEGImages', 'video1')

os.makedirs(destination_folder, exist_ok=True)

def convert_png_to_jpg(source_path, destination_path):
    with Image.open(source_path) as img:
        rgb_img = img.convert('RGB')
        # Try finding code that uses CV's objects for conversion
        destination_path = destination_path.replace('.png', '.jpg')
        rgb_img.save(destination_path, 'JPEG')

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

points = []

def select_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(image_display, (x, y), 3, (0, 255, 0), -1)
        cv2.imshow("Image", image_display)

def create_mask(image, points):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    points_array = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [points_array], 255)
    return mask

image_path = './input/JPEGImages/video1/00000001.jpg'
image = cv2.imread(image_path)
image_display = image.copy()

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", select_points)

print("Click on the image to select points. Press Enter when done.")

while True:
    cv2.imshow("Image", image_display)
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Enter key
        break

mask = create_mask(image, points)
# Make folder if not exist
os.makedirs('./input/Annotations/video1', exist_ok=True)

# Save the mask image
cv2.imwrite('./input/Annotations/video1/00000000.png', mask)

cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

