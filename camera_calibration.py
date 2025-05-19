import numpy as np
import cv2 as cv
import glob
 
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
 
images = glob.glob('chessboard_img/*.png')
 
for fname in images:
    img = cv.imread(fname)
    
    if img is None:
        print("Error: Could not read image ", fname)
        continue
    
    # Resize the image (adjust the new_width and new_height according to your needs)
    #new_width = 1200  # Specify the new width
    #new_height = 800  # Specify the new height
    #img = cv.resize(img, (new_width, new_height))
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (9, 6), None)

    if not ret:
        print("Error: Chessboard corners not found in ", fname)
        continue

    # If found, add object points, image points (after refining them)
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    if corners2 is None:
        print("Error: Failed to refine corners for ", fname)
        continue
    
    # Rescale the corners according to the new image size
    #corners2[:, 0, 0] *= (new_width / img.shape[1])
    #corners2[:, 0, 1] *= (new_height / img.shape[0])
    
    imgpoints.append(corners2)

    # Draw and display the corners
    cv.drawChessboardCorners(img, (9, 6), corners2, ret)
    #cv.imshow('img', img)
    cv.waitKey(0)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
#print('dist:', dist)

fx = mtx[0, 0]  # Focal length along the x-axis
fy = mtx[1, 1]  # Focal length along the y-axis

# Physical size of the sensor or film (sensor size type 1)
sensor_width_mm = 13.2  # Assuming sensor width of 36mm for type 1 sensors
sensor_height_mm = 8.8  # Assuming sensor height of 24mm for type 1 sensors

# Assuming the image resolution is given by gray.shape[::-1]
image_width_pixels = gray.shape[1]
image_height_pixels = gray.shape[0]

# Calculate the size of a pixel in millimeters
pixel_size_x_mm = sensor_width_mm / image_width_pixels
pixel_size_y_mm = sensor_height_mm / image_height_pixels

# Convert focal lengths to millimeters
fx_mm = fx * pixel_size_x_mm
fy_mm = fy * pixel_size_y_mm

print("Focal length along x-axis (mm):", fx_mm)
print("Focal length along y-axis (mm):", fy_mm)

img = cv.imread('chessboard_img/chess6.png')
# Resize the image (adjust the new_width and new_height according to your needs)
#new_width = 600  # Specify the new width
#new_height = 400  # Specify the new height
#img = cv.resize(img, (new_width, new_height))

h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
 
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

#cv.imshow('calibresult', dst)
#cv.imshow('image', img)
cv.imwrite('undistorted.png', dst)
cv.waitKey(0)

#img2=cv.subtract(img,dst)
#cv.imwrite('subt.png', img2)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
 
print( "total error: {}".format(mean_error/len(objpoints)) )
