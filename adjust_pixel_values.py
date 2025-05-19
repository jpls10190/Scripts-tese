import cv2
import functions as fc

img=cv2.imread("imagens_teste/teste2/crateras2.png", cv2.IMREAD_GRAYSCALE)

specific_value = 76
increment_value = 40
img_adjust = fc.adjust_image_values(img, specific_value, increment_value)

# Redimensiona a imagem para um tamanho menor
scale_percent = 25  # Defina a porcentagem em relação à original
width = int(img_adjust.shape[1] * scale_percent / 100)
height = int(img_adjust.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(img_adjust, dim, interpolation=cv2.INTER_AREA)

cv2.imshow('image',image)
cv2.waitKey(0)