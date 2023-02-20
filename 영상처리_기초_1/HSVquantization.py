import cv2 as cv
import numpy as np
import math

roi = cv.imread('lenna.png')

# hsv 바꾸기
hsv_roi = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

model_hist = np.zeros((64,64))

# 양자화
for i in range(hsv_roi.shape[1]):
        for j in range(hsv_roi.shape[0]):
            model_hist[math.trunc(hsv_roi.item(j,i,0)/180*(64-1)),math.trunc(hsv_roi.item(j,i,1)/255)*(64-1)]+=1

cv.imshow('hsv_image',hsv_roi)
cv.waitKey(0)
cv.destroyAllWindows()