import cv2 as cv
import numpy as np

roi = cv.imread('lenna.png')

output = np.zeros((roi.shape[0]//2,roi.shape[1]//2,roi.shape[2]),dtype=np.uint8)

for j in range(output.shape[0]):
    for i in range(output.shape[1]):
        for k in range(3):
            sum = 0
            for r in range(-2,3):
                for c in range(-2,3):
                    y = j*2+r
                    x = i*2+c
                    if y >= 0 and y < roi.shape[0] and x >= 0 and x < roi.shape[1]:
                        sum += roi.item(y,x,k)
            sum /= 25
            output.itemset(j,i,k,int(sum))
cv.imshow('origin',roi)
cv.imshow('result-Mean',output)
cv.waitKey(0)
cv.destroyAllWindows()
