import cv2 as cv
import numpy as np
#smoothing
roi = cv.imread('lenna(gray).jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

prewitt_mask_x = np.array([
    [-1,0,1],
    [-1,0,1],
    [-1,0,1]
])
prewitt_mask_y = np.array([
    [-1,-1,-1],
    [0,0,0],
    [1,1,1]
])
sobel_mask_x = np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
])
sobel_mask_y = np.array([
    [-1,-2,-1],
    [0,0,0],
    [1,2,1]
])
output_prewitt_x = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_prewitt_y = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_sobel_x = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_sobel_y = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
# output_box = np.zeros((roi.shape[0],roi.shape[1])) #float

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += roi_gray.item(j+r,i+c)* prewitt_mask_x.item(r+1,c+1)  #mask 값
        sum = np.abs(sum)
        if sum > 255:
            sum = 255
        # sum /= 255 # 실수의 경우.
        output_prewitt_x.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += roi_gray.item(j+r,i+c)* prewitt_mask_y.item(r+1,c+1)  #mask 값
        sum = np.abs(sum)
        if sum > 255:
            sum = 255
        # sum /= 255 # 실수의 경우.
        output_prewitt_y.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += roi_gray.item(j+r,i+c)* sobel_mask_x.item(r+1,c+1)  #mask 값
        sum = np.abs(sum)
        if sum > 255:
            sum = 255
        # sum /= 255 # 실수의 경우.
        output_sobel_x.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += roi_gray.item(j+r,i+c)* sobel_mask_y.item(r+1,c+1)  #mask 값
        sum = np.abs(sum)
        if sum > 255:
            sum = 255
        # sum /= 255 # 실수의 경우.
        output_sobel_y.itemset(j,i,sum)
cv.imshow('origin',roi_gray)
cv.imshow('output_prewitt_x',output_prewitt_x)
cv.imshow('output_prewitt_y',output_prewitt_y)
cv.imshow('output_sobel_x',output_sobel_x)
cv.imshow('output_sobel_y',output_sobel_y)
cv.waitKey(0)
cv.destroyAllWindows()
