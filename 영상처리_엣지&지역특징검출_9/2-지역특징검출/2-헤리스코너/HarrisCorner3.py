import cv2 as cv
import numpy as np

gaussian_mask = np.array([
    [0.0751,0.1238,0.0751],
    [0.1238,0.2042,0.1238],
    [0.0751,0.1238,0.0751]
    ])

roi = cv.imread('pattern.png')
roi_gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
edge_x = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
edge_y = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
edge_xy = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
edge_x2_gauss = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
edge_y2_gauss = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
edge_xy_gauss = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
result = roi.copy()

for i in range(1,roi_gray.shape[0]-1):
    for j in range(1,roi_gray.shape[1]-1):
        value = roi_gray.item(i,j+1) - roi_gray.item(i,j-1) # dx
        edge_x.itemset(i,j,value)
        value = roi_gray.item(i+1,j) - roi_gray.item(i-1,j) # dy
        edge_y.itemset(i,j,value)

edge_x2 = edge_x**2 # dx^2
edge_y2 = edge_y**2 # dy^2
edge_xy = edge_x * edge_y # dxy

for j in range(1,roi_gray.shape[0]-1):
    for i in range(1,roi_gray.shape[1]-1):
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for r in range(-1,2):
            for c in range(-1,2):
                sum1 += gaussian_mask.item(c+1,r+1) * edge_x2.item(j+c,i+r) # dx^2 * G
                sum2 += gaussian_mask.item(c+1,r+1) * edge_y2.item(j+c,i+r) # dy^2 * G
                sum3 += gaussian_mask.item(c+1,r+1) * edge_xy.item(j+c,i+r) # dxy * G
        edge_x2_gauss.itemset(j,i,sum1)
        edge_y2_gauss.itemset(j,i,sum2)
        edge_xy_gauss.itemset(j,i,sum3)

S = np.zeros((roi_gray.shape[0],roi_gray.shape[1]))
for i in range(roi_gray.shape[0]):
    for j in range(roi_gray.shape[1]):
        det = edge_x2_gauss.item(i,j) * edge_y2_gauss.item(i,j) - edge_xy_gauss.item(i,j)*edge_xy_gauss.item(i,j)
        trace = edge_x2_gauss.item(i,j) + edge_y2_gauss.item(i,j)
        value = det - 0.04 * (trace**2) # C
        S.itemset(i,j,value)
S = cv.dilate(S,None)
T = np.max(S)
result[S > T*0.01] = [0,0,255]

#cv.imshow('edge_x',edge_x)
#cv.imshow('edge_y',edge_y)
#cv.imshow('edge_x2',edge_x2)
#cv.imshow('edge_y2',edge_y2)
#cv.imshow('edge_xy',edge_xy)
cv.imshow('edge_x2_gauss',edge_x2_gauss)
cv.imshow('edge_y2_gauss',edge_y2_gauss)
cv.imshow('edge_xy_gauss',edge_xy_gauss)
cv.imshow('result',result)
cv.waitKey(0)
cv.destroyAllWindows()
