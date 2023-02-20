import cv2 as cv
import numpy as np
import sys

roi = cv.imread('gray_img.jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
new_img_dilation = roi_gray.copy()
new_img_erosion = roi_gray.copy()
ret,thresh = cv.threshold(roi_gray,20,255,0)
thresh = cv.merge((thresh,thresh,thresh))

for i in range(roi_gray.shape[0]):
    for j in range(roi_gray.shape[1]):
        arr = np.zeros(9,dtype=np.uint8)
        index=0
        for r in range(-1,2):
            for c in range(-1,2):
                if i+r < 0 or j+c <0 or i+r > roi_gray.shape[0]-1 or j+c > roi_gray.shape[1]-1:
                    arr.itemset(index,-999)
                else:
                    arr.itemset(index, roi_gray.item(i+r,j+c))
                index+=1
        arr.sort()
        new_img_dilation.itemset(i,j,arr.item(8))
roi_gray2 = new_img_dilation.copy()
for i in range(roi_gray2.shape[0]):
    for j in range(roi_gray2.shape[1]):
        arr = np.zeros(9,dtype=np.uint8)
        index=0
        for r in range(-1,2):
            for c in range(-1,2):
                if i+r < 0 or j+c <0 or i+r > roi_gray2.shape[0]-1 or j+c > roi_gray2.shape[1]-1:
                    arr.itemset(index,-999)
                else:
                    arr.itemset(index, roi_gray2.item(i+r,j+c))
                index+=1
        arr.sort()
        new_img_dilation.itemset(i,j,arr.item(8))

for i in range(roi_gray.shape[0]):
    for j in range(roi_gray.shape[1]):
        arr = np.zeros(9,dtype=np.uint8)
        index=0
        for r in range(-1,2):
            for c in range(-1,2):
                if i+r < 0 or j+c <0 or i+r > roi_gray.shape[0]-1 or j+c > roi_gray.shape[1]-1:
                    arr.itemset(index,999)
                else:
                    arr.itemset(index, roi_gray.item(i+r,j+c))
                index+=1
        arr.sort()
        new_img_erosion.itemset(i,j,arr.item(0))
roi_gray3 = new_img_erosion.copy()
for i in range(roi_gray3.shape[0]):
    for j in range(roi_gray3.shape[1]):
        arr = np.zeros(9,dtype=np.uint8)
        index=0
        for r in range(-1,2):
            for c in range(-1,2):
                if i+r < 0 or j+c <0 or i+r > roi_gray3.shape[0]-1 or j+c > roi_gray3.shape[1]-1:
                    arr.itemset(index,999)
                else:
                    arr.itemset(index, roi_gray3.item(i+r,j+c))
                index+=1
        arr.sort()
        new_img_erosion.itemset(i,j,arr.item(0))

cv.imshow('origin',roi_gray)
cv.imshow('img_dilation',new_img_dilation)
cv.imshow('img_erosion',new_img_erosion)
cv.waitKey(0)
cv.destroyAllWindows()