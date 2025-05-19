from ultralytics import YOLO
from vimba import *
import numpy as np
import cv2
import functions as fc
import tkinter as tk
from PIL import Image, ImageTk

# Import yolo model
model_craters = YOLO('../results/train11/weights/best.pt')
model_scratches = YOLO('....')

def exit_app():
    window.quit()  # Quit the tkinter main loop

# Initialize tkinter window
window = tk.Tk()
window.title("Real-Time Image Display")

# Label to display the image
label = tk.Label(window)
label.pack()

# Exit button
exit_button = tk.Button(window, text="Exit", command=exit_app)
exit_button.pack(pady=10)

mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)

with Vimba.get_instance() as vimba:
    
    camera_id = fc.vimba_getcameraID(vimba)

    with camera_id as camera:
        while True:
            frame = camera.get_frame()
            image_data = frame.as_numpy_ndarray()
            image_data = image_data.astype(np.uint8)

            # Resize image to a smaller size
            scale_percent = 16  # Set percentage relative to original
            img = fc.resize_image(img, scale_percent)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            # Get just the content of the mask / Get the ROI
            img = fc.apply_mask(img, mask)
            
            # Divide image in 6 parts
            [part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8] = fc.divide_image4x2(img)

            # Prediction for craters model on every part
            results1c = model_craters.predict(part_1, show_boxes=True, line_width=1, show=False, conf=0.45)
            results2c = model_craters.predict(part_2, show_boxes=True, line_width=1, show=False, conf=0.45)
            results3c = model_craters.predict(part_3, show_boxes=True, line_width=1, show=False, conf=0.45)
            results4c = model_craters.predict(part_4, show_boxes=True, line_width=1, show=False, conf=0.45)
            results5c = model_craters.predict(part_5, show_boxes=True, line_width=1, show=False, conf=0.45)
            results6c = model_craters.predict(part_6, show_boxes=True, line_width=1, show=False, conf=0.45)
            results7c = model_craters.predict(part_7, show_boxes=True, line_width=1, show=False, conf=0.45)
            results8c = model_craters.predict(part_8, show_boxes=True, line_width=1, show=False, conf=0.45)

            # Prediction for scratches model on every part
            results1s = model_scratches.predict(part_1, show_boxes=True, line_width=1, show=False, conf=0.45)
            results2s = model_scratches.predict(part_2, show_boxes=True, line_width=1, show=False, conf=0.45)
            results3s = model_scratches.predict(part_3, show_boxes=True, line_width=1, show=False, conf=0.45)
            results4s = model_scratches.predict(part_4, show_boxes=True, line_width=1, show=False, conf=0.45)
            results5s = model_scratches.predict(part_5, show_boxes=True, line_width=1, show=False, conf=0.45)
            results6s = model_scratches.predict(part_6, show_boxes=True, line_width=1, show=False, conf=0.45)
            results7s = model_scratches.predict(part_7, show_boxes=True, line_width=1, show=False, conf=0.45)
            results8s = model_scratches.predict(part_8, show_boxes=True, line_width=1, show=False, conf=0.45)

            resultsc = [results1c, results2c, results3c, results4c, results5c, results6c, results7c, results8c]
            resultss = [results1s, results2s, results3s, results4s, results5s, results6s, results7s, results8s]

            number_craters = 0
            number_scratches = 0

            for part in range(8):
                resultcr=resultsc[part]
                resultsc=resultsc[part]
                for i, res in enumerate(resultcr):  
                    print(f"Result {i + 1}:")
                    
                    # Access the bounding boxes for each result
                    boxes = res.boxes       

                    number_cratersx = len(boxes)
                    number_craters = number_craters + number_cratersx

                    # Extract information from the boxes
                    if boxes is not None:
                        # Access the coordinates in xyxy format (x1, y1, x2, y2)
                        coordinates = boxes.xyxy.cpu().numpy()  # Convert to NumPy array
                        print("Bounding box coordinates (xyxy):", coordinates)

                        # Access the confidence scores
                        confidences = boxes.conf.cpu().numpy()  # Convert to NumPy array
                        print("Confidence scores:", confidences)

                        # Access the class predictions
                        classes = boxes.cls.cpu().numpy()  # Convert to NumPy array
                        print("Class predictions:", classes)

                        # Optionally, access other formats like xywh (center x, center y, width, height)
                        coordinates_xywh = boxes.xywh.cpu().numpy()  # Convert to NumPy array
                        print("Bounding box coordinates (xywh):", coordinates_xywh)

                        # Corresponding class names
                        class_names = res.names

                        # For every bounding box, draw on the image the rectangle, confidence score, and label  
                        for j in range(len(coordinates)):
                            x1, y1, x2, y2 = coordinates[j]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to standard Python integers
                            x1, y1, x2, y2 = fc.get_coords(x1,y1,x2,y2,part,img)
                            
                            score = confidences[j]
                            class_id = classes[j]

                            # Get the class name using the class id
                            class_name = class_names[int(class_id)]

                            color = (0, 0, 255)
                            color_rgb = (color[2], color[1], color[0])
                            cv2.rectangle(img, (x1, y1), (x2, y2), color_rgb, 1)
                            cv2.putText(img, f"{class_name} {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                for i, res in enumerate(resultsc):  
                    print(f"Result {i + 1}:")
                    
                    # Access the bounding boxes for each result
                    boxes = res.boxes       

                    number_scratchesx = len(boxes)
                    number_scratches = number_scratches + number_scratchesx

                    # Extract information from the boxes
                    if boxes is not None:
                        # Access the coordinates in xyxy format (x1, y1, x2, y2)
                        coordinates = boxes.xyxy.cpu().numpy()  # Convert to NumPy array
                        print("Bounding box coordinates (xyxy):", coordinates)

                        # Access the confidence scores
                        confidences = boxes.conf.cpu().numpy()  # Convert to NumPy array
                        print("Confidence scores:", confidences)

                        # Access the class predictions
                        classes = boxes.cls.cpu().numpy()  # Convert to NumPy array
                        print("Class predictions:", classes)

                        # Optionally, access other formats like xywh (center x, center y, width, height)
                        coordinates_xywh = boxes.xywh.cpu().numpy()  # Convert to NumPy array
                        print("Bounding box coordinates (xywh):", coordinates_xywh)

                        # Corresponding class names
                        class_names = res.names

                        # For every bounding box, draw on the image the rectangle, confidence score, and label  
                        for j in range(len(coordinates)):
                            x1, y1, x2, y2 = coordinates[j]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to standard Python integers
                            x1, y1, x2, y2 = fc.get_coords(x1,y1,x2,y2,part,img)
                            
                            score = confidences[j]
                            class_id = classes[j]

                            # Get the class name using the class id
                            class_name = class_names[int(class_id)]

                            color = (0, 0, 255)
                            color_rgb = (color[2], color[1], color[0])
                            cv2.rectangle(img, (x1, y1), (x2, y2), color_rgb, 1)
                            cv2.putText(img, f"{class_name} {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            
            # OK : Max 1 crater and 0 scratches

            # Printing if it is OK or NOT OK and how many defects
            if number_craters < 2 and number_scratches == 0:
                text_label = tk.Label(window, text="OK: " + number_craters + " craters and " + number_scratches + " scratches.")
                text_label.pack()
            else:
                text_label = tk.Label(window, text="NOT OK: " + number_craters + " craters and " + number_scratches + " scratches.")
                text_label.pack()
                
            # Convert numpy array to PIL Image
            img = Image.fromarray(img)

            # Convert PIL Image to Tkinter PhotoImage
            img = ImageTk.PhotoImage(img)
            
            # Update label with new image
            label.configure(image=img)
            label.image = img  # keep a reference

            window.update_idletasks()  # Update the tkinter window
            window.update()  # Allow tkinter to process events

window.mainloop()
