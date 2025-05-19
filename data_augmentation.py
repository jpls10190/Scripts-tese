import os
import cv2
import numpy as np
from PIL import Image

def load_images_and_labels(image_dir, label_dir):
    images = []
    labels = []
    for image_file in os.listdir(image_dir):
        if image_file.endswith('.jpg') or image_file.endswith('.png'):
            image_path = os.path.join(image_dir, image_file)
            label_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))

            image = cv2.imread(image_path)
            images.append((image_file, image))

            with open(label_path, 'r') as file:
                boxes = [line.strip().split() for line in file.readlines()]
                labels.append((image_file, boxes))
    return images, labels

image_dir = './images'
label_dir = './labels'
images, labels = load_images_and_labels(image_dir, label_dir)

def adjust_exposure(image, factor):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.convertScaleAbs(hsv[:, :, 2], alpha=factor, beta=0)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def vertical_flip(image, boxes):
    flipped_image = cv2.flip(image, 0)
    height = image.shape[0]
    flipped_boxes = []
    for box in boxes:
        cls, x_center, y_center, width, height = map(float, box)
        y_center = 1.0 - y_center  # Flip the y_center
        flipped_boxes.append([cls, x_center, y_center, width, height])
    return flipped_image, flipped_boxes

def horizontal_flip(image, boxes):
    flipped_image = cv2.flip(image, 1)  # Flip horizontally
    width = image.shape[1]
    flipped_boxes = []
    for box in boxes:
        cls, x_center, y_center, w, h = map(float, box)
        x_center = 1.0 - x_center  # Flip the x_center
        flipped_boxes.append([cls, x_center, y_center, w, h])
    return flipped_image, flipped_boxes

def save_augmented_data(image, boxes, image_name, output_image_dir, output_label_dir, suffix):
    output_image_path = os.path.join(output_image_dir, f"{image_name}_{suffix}.jpg")
    output_label_path = os.path.join(output_label_dir, f"{image_name}_{suffix}.txt")

    cv2.imwrite(output_image_path, image)

    with open(output_label_path, 'w') as file:
        for box in boxes:
            file.write(" ".join(map(str, box)) + "\n")

output_image_dir = './newimages'
output_label_dir = './newlabels'
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

for (image_name, image), (label_name, boxes) in zip(images, labels):

    exposed_image = adjust_exposure(image, 0.75)
    save_augmented_data(exposed_image, boxes, image_name, output_image_dir, output_label_dir, 'exposed_0_75')

    # Adjust exposure
    exposed_image = adjust_exposure(image, 1.25)
    save_augmented_data(exposed_image, boxes, image_name, output_image_dir, output_label_dir, 'exposed_1_25')

    # Flip vertically
    flipped_image, flipped_boxes = vertical_flip(image, boxes)
    save_augmented_data(flipped_image, flipped_boxes, image_name, output_image_dir, output_label_dir, 'flippedV')

    # Flip horizontally
    flipped_image, flipped_boxes = horizontal_flip(image, boxes)
    save_augmented_data(flipped_image, flipped_boxes, image_name, output_image_dir, output_label_dir, 'flippedH')