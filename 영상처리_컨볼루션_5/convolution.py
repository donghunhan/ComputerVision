import cv2 as cv
import numpy as np

gaussian_mask = np.array([
    [0.0000,0.0000,0.0002,0.0000,0.0000],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0002,0.0837,0.6187,0.0837,0.0002],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0000,0.0000,0.0002,0.0000,0.0000]])

sharpening_mask = np.array([
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]
])

motion_mask = np.array([
    [0.0304,0.0501,0,0,0],
    [0.0501,0.01771,0.0519,0,0],
    [0,0.0519,0.01771,0.0519,0],
    [0,0,0.0519,0.01771,0.0501],
    [0,0,0,0.0501,0.0304]
])

roi = cv.imread('picture5.jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

output_box = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_gaussian = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_sharpening = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_horizon = np.zeros((roi.shape[0],roi.shape[1]))
output_vertical = np.zeros((roi.shape[0],roi.shape[1]))
output_motion = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)


for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += roi_gray.item(j+r,i+c)
        sum //= 9
        output_box.itemset(j,i,sum)

for j in range(2,roi.shape[0]-2):
    for i in range(2,roi.shape[1]-2):
        sum = 0
        for r in range(-2,3):
            for c in range(-2,3):
                sum += gaussian_mask.item(r+2,c+2) * roi_gray.item(j+r,i+c)
        int(sum)
        output_gaussian.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum += sharpening_mask.item(r+1,c+1) * roi_gray.item(j+r,i+c)
        output_sharpening.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0.0
        sum += roi_gray.item(j-1,i-1) - roi_gray.item(j+1,i-1)
        sum += roi_gray.item(j-1,i) - roi_gray.item(j+1,i)
        sum += roi_gray.item(j-1,i+1) - roi_gray.item(j+1,i+1)
        sum /= 255.0
        output_horizon.itemset(j,i,sum)

for j in range(1,roi.shape[0]-1):
    for i in range(1,roi.shape[1]-1):
        sum = 0.0
        sum += roi_gray.item(j-1,i-1) - roi_gray.item(j-1,i+1)
        sum += roi_gray.item(j,i-1) - roi_gray.item(j,i+1)
        sum += roi_gray.item(j+1,i-1) - roi_gray.item(j+1,i+1)
        sum /= 255.0
        output_vertical.itemset(j,i,sum)

for j in range(2,roi.shape[0]-2):
    for i in range(2,roi.shape[1]-2):
        sum = 0
        for r in range(-2,3):
            for c in range(-2,3):
                sum += motion_mask.item(r+2,c+2) * roi_gray.item(j+r,i+c)
        int(sum)
        output_motion.itemset(j,i,sum)

cv.imshow('origin',roi_gray)
cv.imshow('box_mask',output_box)
cv.imshow('gaussian_mask',output_gaussian)
cv.imshow('sharpening_mask',output_sharpening)
cv.imshow('horizontal_edge',output_horizon)
cv.imshow('vertical_edge',output_vertical)
cv.imshow('motion_mask',output_motion)

cv.waitKey(0)
cv.destroyAllWindows()