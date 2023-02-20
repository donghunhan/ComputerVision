import cv2 as cv
import numpy as np
import sys

roi = cv.imread('OpenClose-binary-test.bmp')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
new_img = roi_gray.copy()
ret,thresh = cv.threshold(roi_gray,20,255,0)
thresh = cv.merge((thresh,thresh,thresh))

while True:
    num = int(input("(0: Erosion 1: Dilation 999: exit) :"))
    if num == 999:
        break
    elif num == 0:
        for i in range(1,roi_gray.shape[0]-1):
            for j in range(1,roi_gray.shape[1]-1):
                if roi_gray.item(i,j) == 255:
                    count = 0
                    for r in range(-1,2):
                        for c in range(-1,2):
                            if roi_gray.item(i+r,j+c)==255 :
                                count+=1
                    if count < 9:
                        new_img.itemset(i,j,0)
    elif num == 1:
        for i in range(1,roi_gray.shape[0]-1):
            for j in range(1,roi_gray.shape[1]-1):
                if roi_gray.item(i,j) == 0:
                    count = 0
                    for r in range(-1,2):
                        for c in range(-1,2):
                            if roi_gray.item(i+r,j+c)==255 :
                                count+=1
                    if count > 0:
                        new_img.itemset(i,j,255)
    else:
        print('wrong input!')
    cv.imshow('img',new_img)
    cv.waitKey(0)
    roi_gray = new_img.copy()
cv.destroyAllWindows()
