import cv2 as cv
import numpy as np

roi = cv.imread('pic1.jpg')
binary = np.zeros((roi.shape[0],roi.shape[1],roi.shape[2]),dtype=np.uint8)
# Opencv에서 imread함수를 사용하면 흑백이미지여도, rgb 3채널로 입력된다.

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        if (roi.item(i,j,0) >= 127):
            binary.itemset(i,j,0,255)
            binary.itemset(i,j,1,255)
            binary.itemset(i,j,2,255)
        else:
            binary.itemset(i,j,0,0)
            binary.itemset(i,j,1,0)
            binary.itemset(i,j,2,0)

cv.imshow('roi',roi)
cv.imshow('binary',binary)
cv.waitKey(0)
cv.destroyAllWindows()