import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('gamma_correction')

cv.createTrackbar('gamma','gamma_correction',0,500,nothing)

cv.setTrackbarPos('gamma','gamma_correction', 100)

roi = cv.imread('picture2.jpg')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

output = np.zeros((roi.shape[0],roi.shape[1]),dtype=np.uint8)

while True:

    g = cv.getTrackbarPos('gamma','gamma_correction') / 100 # 0.0 ~ 5.0

    for i in range(roi.shape[1]):
        for j in range(roi.shape[0]):
            output.itemset(j,i,255 * (roi_gray.item(j,i)/255)**g) # 2.12 수식.
    
    cv.imshow('gamma_correction',output)

    if cv.waitKey(1) & 0xFF == 27: # ESC를 누르면 종료
        break

cv.destroyAllWindows()