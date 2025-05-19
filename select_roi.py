import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from vimba import *

# Initialize variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1
rect = (0, 0, 1, 1)  # Initial rectangle
mask = None

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rect, mask

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        rect = (x, y, x, y)
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Update rectangle dimensions
            rect = (ix, iy, x, y)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Final rectangle dimensions
        rect = (ix, iy, x, y)
        # Create mask based on the selected rectangle
        mask = np.zeros_like(img)
        mask[min(iy, y):max(iy, y), min(ix, x):max(ix, x)] = 255
        cv2.imshow('mask', mask)

# Create a window and set the mouse callback
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", draw_rectangle)

with Vimba.get_instance() as vimba:
    # List of available cameras
    camera_ids = vimba.get_all_cameras()
    print(f"Found {len(camera_ids)} camera(s)")
    
    if len(camera_ids) == 0:
        print('No cameras found')
        exit()

    # Print available cameras
    print('Available cameras:')
    for camera_id in camera_ids:
        print(camera_id)
    
    # Open the first camera
    camera_id = camera_ids[0]  

    with camera_id as camera:
        while True:
            frame = camera.get_frame()
            image_data = frame.as_numpy_ndarray()
            image_data = image_data.astype(np.uint8)
            # Resize image to a smaller size
            scale_percent = 16  # Set percentage relative to original
            width = int(image_data.shape[1] * scale_percent / 100)
            height = int(image_data.shape[0] * scale_percent / 100)
            dim = (width, height)
            img = cv2.resize(image_data, dim, interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            # Make a copy of the current frame to draw the rectangle on
            frame_copy = img.copy()

            # Draw the rectangle in the live image
            if drawing or mask is not None:
                cv2.rectangle(frame_copy, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)

            cv2.imshow("Video",frame_copy)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if mask is not None:
                    cv2.imwrite('mask.png', mask)
                    print("ROI saved as 'mask.png'")
                break
        
    cv2.destroyAllWindows()