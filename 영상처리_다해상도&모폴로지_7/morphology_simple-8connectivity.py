# 이름 
import cv2 as cv
import numpy as np
import sys

roi = cv.imread('OpenClose-binary-test.bmp')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
new_img_dilation = roi_gray.copy()
new_img_erosion = roi_gray.copy()
ret,thresh = cv.threshold(roi_gray,127,255,0)

for i in range(1,roi_gray.shape[0]-1):
    for j in range(1,roi_gray.shape[1]-1):
        if roi_gray.item(i,j) == 255:
            count = 0
            for r in range(-1,2):
                for c in range(-1,2):
                    if roi_gray.item(i+r,j+c)==255 :
                        count+=1
            if count < 9:
                new_img_erosion.itemset(i,j,0)

for i in range(1,roi_gray.shape[0]-1):
    for j in range(1,roi_gray.shape[1]-1):
        if roi_gray.item(i,j) == 0:
            count = 0
            for r in range(-1,2):
                for c in range(-1,2):
                    if roi_gray.item(i+r,j+c)==255 :
                        count+=1
            if count > 0:
                new_img_dilation.itemset(i,j,255)

cv.imshow('origin',roi_gray)
cv.imshow('img_dilation',new_img_dilation)
cv.imshow('img_erosion',new_img_erosion)
cv.waitKey(0)
cv.destroyAllWindows()