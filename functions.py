import cv2
import numpy as np

#Definir novos parâmetros da câmara
def novos_parametros(xmlfile, exposicao, ganho):
    with open(xmlfile, 'r') as ficheiro:
        linhas = ficheiro.readlines()
        linha_exposicao = '\t'+'\t<Feature Name="ExposureTime" Type="Float" Access="R/W">'+str(exposicao)+'</Feature>\n'
        linha_ganho = '\t'+'\t<Feature Name="Gain" Type="Float" Access="R/W">'+str(ganho)+'</Feature>\n'
        linhas[40]=linha_exposicao
        linhas[53]=linha_ganho

        #print(linhas[24])

    with open(xmlfile, 'w') as ficheiro:
        ficheiro.write("")
    with open(xmlfile, 'w') as ficheiro:
        ficheiro.writelines(linhas)

#Remover segmentos menores que threshold
def remove_segments(img, threshold):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

    result_mask = np.zeros_like(img)

    for label in range(1, num_labels):
        # Check if the area is greater than the threshold
        if stats[label, cv2.CC_STAT_AREA] >= threshold:
            # Add the connected component to the result mask
            result_mask[labels == label] = 255
    return result_mask

#Iterar para todos os objetos de uma imagem binarizada
def iterate_all_objects(binary_image):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    # Iterate over each connected component
    for label in range(1, num_labels):  # Skip background label (label=0)
        # Create a mask for the current connected component
        component_mask = np.uint8(labels == label) * 255

        # Perform any operations on the current connected component
        # Example: Save or process the component
        cv2.imshow(f"Connected Component {label}", component_mask)
        cv2.waitKey(0)

#Iterar para todos os objetos de uma imagem binarizada e obter o label x
def get_object(binary_image, x):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    # Iterate over each connected component
    for label in range(1, num_labels):  # Skip background label (label=0)
        # Create a mask for the current connected component
        component_mask = np.uint8(labels == label) * 255
        if label==x:
            return component_mask

#Obter valores maximos e minimos onde a imagem não é 0
def getmaxmin_img(img):
    xshape=img.shape[0]
    yshape=img.shape[1]

    for x in range(xshape):
        img_line = img[x,:]
        if sum(img_line)!=0:
            minx=x
            break
    for x in range(xshape):
        img_line = img[xshape-x-1,:]
        if sum(img_line)!=0:
            maxx=xshape-x-1
            break
    for y in range(yshape):
        img_column = img[:,y]
        if sum(img_column)!=0:
            miny=y
            break
    for y in range(yshape):
        img_column = img[:,yshape-y-1]
        if sum(img_column)!=0:
            maxy=yshape-y-1
            break
        
    return minx,miny,maxx,maxy            

import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = []
    for obj in root.findall('object'):
        label = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        data.append((label, (xmin, ymin, xmax, ymax)))
    
    return data

def write_to_txt(data, txt_file):
    with open(txt_file, 'w') as f:
        for label, bbox in data:
            line = f"{txt_file.split('.')[0]} {bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},{label}\n"
            f.write(line)

def convert_xml_to_txt_annotations(xml_path, txtfilename):

    # Parse XML file
    data = parse_xml(xml_path)

    # Write data to text file
    write_to_txt(data, txtfilename)

def add_gaussian_noise(img):
    # Generate random Gaussian noise
    mean = 0
    stddev = 180
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, mean, stddev)

    # Add noise to image
    noisy_img = cv2.add(img, noise)

    # Save noisy image
    cv2.imwrite('noisy_img.jpg', noisy_img)

def adjust_pixel_value(pixel, specific_value, increment_value):
    if pixel > specific_value:
        return pixel + increment_value
    elif pixel < specific_value:
        return pixel - increment_value
    else:
        return pixel

def adjust_image_values(image, specific_value, increment_value):
    adjusted_image = np.copy(image)
    rows, cols = image.shape

    for i in range(rows):
        for j in range(cols):
            adjusted_image[i, j] = adjust_pixel_value(image[i, j], specific_value, increment_value)

    return adjusted_image

def divide_image_3x2(img):
    # Get the dimensions of the image
    height, width, _ = img.shape

    # Calculate the dimensions of each part
    part_height = height // 3
    part_width = width // 2

    # Extract each part and save into variables
    part_1 = img[0:part_height, 0:part_width]
    part_2 = img[0:part_height, part_width:2*part_width]
    part_3 = img[part_height:2*part_height, 0:part_width]
    part_4 = img[part_height:2*part_height, part_width:2*part_width]
    part_5 = img[2*part_height:height, 0:part_width]
    part_6 = img[2*part_height:height, part_width:2*part_width]

    return part_1, part_2, part_3, part_4, part_5, part_6

def divide_image4x2(img):
    # Get the dimensions of the image
    height, width, _ = img.shape

    # Calculate the dimensions of each part
    part_height = height // 4
    part_width = width // 2

    # Extract each part and save into variables
    part_1 = img[0:part_height, 0:part_width]
    part_2 = img[0:part_height, part_width:2*part_width]
    part_3 = img[part_height:2*part_height, 0:part_width]
    part_4 = img[part_height:2*part_height, part_width:2*part_width]
    part_5 = img[2*part_height:3*part_height, 0:part_width]
    part_6 = img[2*part_height:3*part_height, part_width:2*part_width]
    part_7 = img[3*part_height:height, 0:part_width]
    part_8 = img[3*part_height:height, part_width:2*part_width]

    return part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8

def get_coords(x1, y1, x2, y2, r, img):
    # Get the dimensions of the image
    height, width, _ = img.shape

    # Calculate the dimensions of each part
    part_height = height // 4
    part_width = width // 2

    if r == 1:
        x1 = part_width + x1
        x2 = part_width + x2
    elif r == 2:
        y1 = part_height + y1
        y2 = part_height + y2
    elif r == 3:
        y1 = part_height + y1
        y2 = part_height + y2
        x1 = part_width + x1
        x2 = part_width + x2
    elif r == 4:
        y1 = 2*part_height + y1
        y2 = 2*part_height + y2
    elif r == 5:
        y1 = 2*part_height + y1
        y2 = 2*part_height + y2
        x1 = part_width + x1
        x2 = part_width + x2
    elif r == 6:
        y1 = 3*part_height + y1
        y2 = 3*part_height + y2
    elif r == 7:
        y1 = 3*part_height + y1
        y2 = 3*part_height + y2
        x1 = part_width + x1
        x2 = part_width + x2
    return x1, y1, x2, y2
    
def vimba_getcameraID(vimba):
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

    return camera_id

# resize image to a smaller size: 
# scale -> Set percentage relative to original
def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

# given an image and a mask, create a new image just with the content of the mask in the original image  
def apply_mask(img, mask):
    # Find contours in the mask image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming there's only one white square, get the bounding box of the white square
    x, y, w, h = cv2.boundingRect(contours[0])

    # Extract the content from the original image using the bounding box coordinates
    img = img[y:y+h, x:x+w]

    return img