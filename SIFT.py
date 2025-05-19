import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

img=cv2.imread("imagens_teste/img4.png")

scale_percent = 25  
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

surf = cv2.ORB_create()
kp,des = surf.detectAndCompute(img,None)

bf=cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

template=cv2.imread("img/template.png")

kpt,dest=surf.detectAndCompute(template,None)

matches=bf.match(dest,des)
matches=sorted(matches, key=lambda x:x.distance)

src_pts=np.float32([kpt[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
dst_pts=np.float32([kp[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
M,mask=cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
matchesMask=mask.ravel().tolist()

draw_params = dict(matchColor=(0,255,0),
                   singlePointColor=None,
                   matchesMask = matchesMask,
                   flags=2)

img2=cv2.drawMatches(template,kpt,img,kp,matches,None,**draw_params)

#cv2.imshow('Matches',img2)
#cv2.waitKey(0)