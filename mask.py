import cv2
import os
import numpy as np

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


image_path = './input/JPEGImages/video1/1668813025164826994.jpg'
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
cv2.imwrite('./input/Annotations/video1/1668813025164826994.png', mask)

cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
