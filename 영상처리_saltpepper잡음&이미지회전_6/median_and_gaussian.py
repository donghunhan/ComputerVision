import cv2 as cv
import numpy as np

gaussian_mask = np.array([
    [0.0000,0.0000,0.0002,0.0000,0.0000],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0002,0.0837,0.6187,0.0837,0.0002],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0000,0.0000,0.0002,0.0000,0.0000]])

roi = cv.imread('saltpepper.jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

output_gaussian = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
output_median = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)

for j in range(2,roi.shape[0]-2):
    for i in range(2,roi.shape[1]-2):
        sum = 0
        for r in range(-2,3):
            for c in range(-2,3):
                sum += gaussian_mask.item(c+2,r+2) * roi_gray.item(j+c,i+r)
        int(sum)
        output_gaussian.itemset(j,i,sum)

for j in range(2,roi.shape[0]-2):
    for i in range(2,roi.shape[1]-2):
        mid = 0
        k = 0
        narray = np.zeros(25,dtype=np.uint8)
        for r in range(-2,3):
            for c in range(-2,3):
                narray.itemset(k,roi_gray.item(j+c,i+r))
                k+=1
        narray.sort()
        mid = narray.item(25//2)
        output_median.itemset(j,i,mid)

cv.imshow('origin',roi_gray)
cv.imshow('median',output_median)
cv.imshow('gaussian',output_gaussian)
cv.waitKey(0)
cv.destroyAllWindows()