import cv2 as cv
import numpy as np
import math

roi = cv.imread('lenna.png')

angle = 10.0 #degree

angle = -angle * (math.pi/180) # radian

normal_rotation = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8)
normal_interpolation = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8)
bilinear_interpolation = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        for k in range(3):
            cy = roi.shape[0] // 2
            cx = roi.shape[1] // 2
            y = i - cy
            x = j - cx
            newY = y * math.cos(angle) - x * math.sin(angle) + cy
            newX = y * math.sin(angle) + x * math.cos(angle) + cx
            newY = round(newY)
            newX = round(newX)
            if newX >=0 and newX < roi.shape[1] and newY >=0 and newY < roi.shape[0]:
                normal_rotation.itemset(newY,newX,k,roi.item(i,j,k))

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        for k in range(3):
            cy = roi.shape[0] // 2
            cx = roi.shape[1] // 2
            y = i - cy
            x = j - cx
            newY = y * math.cos(angle) + x * math.sin(angle) + cy
            newX = y * -math.sin(angle) + x * math.cos(angle) + cx
            newY = round(newY)
            newX = round(newX)
            if newX >=0 and newX < roi.shape[1] and newY >=0 and newY < roi.shape[0]:
                normal_interpolation.itemset(i,j,k,roi.item(newY,newX,k))

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        for k in range(3):
            cy = roi.shape[0] // 2
            cx = roi.shape[1] // 2
            y = i - cy
            x = j - cx
            newY = y * math.cos(angle) + x * math.sin(angle) + cy
            newX = y * -math.sin(angle) + x * math.cos(angle) + cx
            alpha = 1 - (newX-math.floor(newX))  # 정수 값 x축에서 떨어진 거리
            beta = 1 - (newY-math.floor(newY)) # 정수 값 y축에서 떨어진 거리
            newX = round(newX)
            newY = round(newY)
            if newX >=0 and newX < roi.shape[1]-1 and newY >=0 and newY < roi.shape[0]-1:
                f1 = (1-alpha)*roi.item(newY,newX,k)+alpha*roi.item(newY,newX+1,k)
                f2 = (1-alpha)*roi.item(newY+1,newX,k)+alpha*roi.item(newY+1,newX+1,k)
                f3 = (1-beta)*f1+beta*f2
                bilinear_interpolation.itemset(i,j,k,int(f3))

cv.imshow('origin',roi)
cv.imshow('rotation_normal',normal_rotation)
cv.imshow('interpolation_normal',normal_interpolation)
cv.imshow('interpolation_bilinear',bilinear_interpolation)
cv.waitKey(0)
cv.destroyAllWindows()
