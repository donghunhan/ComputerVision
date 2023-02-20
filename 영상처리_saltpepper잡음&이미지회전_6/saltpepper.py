import cv2 as cv
import numpy as np
import random

roi = cv.imread('lenna(gray).jpg')

saltpepper_img = roi.copy()

noise_amount = (roi.shape[0]*roi.shape[1])*0.1

for i in range(int(noise_amount)):
    row = random.randint(0,roi.shape[0]-1)
    col = random.randint(0,roi.shape[1]-1)
    value = random.choice([255,0])
    for j in range(3):
        saltpepper_img.itemset(row,col,j,value)

cv.imwrite('./saltpepper.jpg',saltpepper_img)
cv.imshow('saltpepper',saltpepper_img)
cv.imshow('origin',roi)
cv.waitKey(0)
cv.destroyAllWindows()
