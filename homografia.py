import cv2
import numpy as np

img_path='imagens_teste/img1.png'
img=cv2.imread(img_path)
#_, bin_img = cv2.threshold(img,80,255,cv2.THRESH_BINARY)
dim=(1024,768)
img=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
count=0
coords=[]

while True:
    cv2.imshow("bin image", img)

    def mouse_handler(event,x,y,flags,params):
        global count
        global coords

        if event == cv2.EVENT_LBUTTONDOWN:
            count=count+1
            coords.append([x,y])
            print(x,y)
            if count==4:
                return
    cv2.setMouseCallback("bin image", mouse_handler)
    if count==4:
        break
    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit the loop
        break

cv2.destroyAllWindows()
coords=np.array(coords)
pts_dest = np.array([[0,0],[0,768],[1024,768],[1024,0]])
h, status = cv2.findHomography(coords,pts_dest)
im_out = cv2.warpPerspective(img, h, (img.shape[1],img.shape[0]))

#cv2.imwrite("imagens_teste\\img3h.png",im_out)
cv2.imshow("Source Image", img)
cv2.imshow("Warped Source Image", im_out)
cv2.waitKey(0)
