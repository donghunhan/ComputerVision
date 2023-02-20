import cv2 as cv
import numpy as np
#smoothing
roi = cv.imread('lenna(gray).jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

mask = np.array([
    [0.0000,0.0000,0.0002,0.0000,0.0000],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0002,0.0837,0.6187,0.0837,0.0002],
    [0.0000,0.0113,0.0837,0.0113,0.0000],
    [0.0000,0.0000,0.0002,0.0000,0.0000]])

output_box = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)
#output_box = np.zeros((roi.shape[0],roi.shape[1])) #float

for j in range(2,roi.shape[0]-2):
    for i in range(2,roi.shape[1]-2):
        sum = 0
        for r in range(-2,3):
            for c in range(-2,3):
                sum += roi_gray.item(j+r,i+c)* mask.item(r+2,c+2)  #mask 값
        if np.sum(mask) > 0:
            sum //= np.sum(mask)  # mask 요소값의 합
        # sum = np.abs(sum)
        # sum /= 255 # 0.0 ~ 1.0 사이의 값으로 변환
        output_box.itemset(j,i,sum)

cv.imshow('origin',roi_gray)
cv.imshow('box_mask',output_box)
cv.waitKey(0)
cv.destroyAllWindows()