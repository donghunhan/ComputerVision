import cv2 as cv
import numpy as np

roi = cv.imread('lenna.png')
Burt83a_mask = np.array([
    [0.0025,0.0125,0.0200,0.0125,0.0025],
    [0.0125,0.0625,0.1000,0.0625,0.0125],
    [0.0200,0.1000,0.1600,0.1000,0.0200],
    [0.0125,0.0625,0.1000,0.0625,0.0125],
    [0.0025,0.0125,0.0200,0.0125,0.0025]])

print(np.sum(Burt83a_mask)) # 마스크 총합

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
                        sum += Burt83a_mask.item(r+2,c+2) * roi.item(y,x,k)
            output.itemset(j,i,k,int(sum))
cv.imshow('origin',roi)
cv.imshow('result-Burt83a',output)
cv.waitKey(0)
cv.destroyAllWindows()
