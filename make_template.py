import cv2
import numpy as np
import functions as fc

img=cv2.imread("imagens_teste/img1.png")
dim=(1024,768)
img=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img2=cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                           cv2.THRESH_BINARY, 131, 1)

#Remover segmentos menores que x

img2=fc.remove_segments(img2,10000)

#fc.iterate_all_objects(img2)

img3=fc.get_object(img2, 3)

k=np.ones((5,5), np.uint8)
img3=cv2.dilate(img3, k, iterations=15)
img3=cv2.erode(img3, k, iterations=15)

cv2.imshow('img0',img)
cv2.imshow('mask',img3)
img_final=cv2.bitwise_and(img,img,mask=img3)
mx, my, Mx, My = fc.getmaxmin_img(img3)

img_t=img_final[mx:Mx,my:My]

#cv2.imwrite("img/template.png", img_t)
cv2.imshow("Template Image", img_t)
cv2.waitKey(0)