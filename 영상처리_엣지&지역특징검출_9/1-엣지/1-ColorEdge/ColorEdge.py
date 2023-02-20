import cv2 as cv
import numpy as np
import math

SOBEL_Y = np.array([
    [-1,-2,-1],
    [0,0,0],
    [1,2,1]
])
SOBEL_X = np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
])

FILE_NAME = "1.jpg"

roi = cv.imread(FILE_NAME)
edge = cv.Canny(roi,50,150)

red_dx = np.zeros((roi.shape[0],roi.shape[1]))
red_dy = np.zeros((roi.shape[0],roi.shape[1]))

green_dx = np.zeros((roi.shape[0],roi.shape[1]))
green_dy =np.zeros((roi.shape[0],roi.shape[1]))

blue_dx = np.zeros((roi.shape[0],roi.shape[1]))
blue_dy = np.zeros((roi.shape[0],roi.shape[1]))

grad_yy = np.zeros((roi.shape[0],roi.shape[1]))
grad_xx = np.zeros((roi.shape[0],roi.shape[1]))
grad_yx = np.zeros((roi.shape[0],roi.shape[1]))

Ave_map = np.zeros((roi.shape[0],roi.shape[1]))

Ave_edge = np.zeros((roi.shape[0],roi.shape[1]))

Edge_D = np.zeros((roi.shape[0],roi.shape[1]))
Edge_S = np.zeros((roi.shape[0],roi.shape[1]))

ColorEdge_x = np.zeros((roi.shape[0],roi.shape[1],3))
ColorEdge_y = np.zeros((roi.shape[0],roi.shape[1],3))

Dizenzo = np.zeros((roi.shape[0],roi.shape[1]))

for i in range(1,roi.shape[0]-1):
    for j in range(1,roi.shape[1]-1):
        value1 = 0
        value2 = 0
        for r in range(-1,2):
            for c in range(-1,2):
                value1 += SOBEL_X.item(r+1,c+1) * roi.item(i+r,j+c,0)
                value2 += SOBEL_Y.item(r+1,c+1) * roi.item(i+r,j+c,0)
        value1 = abs(value1)
        value2 = abs(value2)
        if value1>255:
            value1=255
        if value2>255:
            value2=255
        value1/=255
        value2/=255
        blue_dx.itemset(i,j,value1)
        blue_dy.itemset(i,j,value2)

for i in range(1,roi.shape[0]-1):
    for j in range(1,roi.shape[1]-1):
        value1 = 0
        value2 = 0
        for r in range(-1,2):
            for c in range(-1,2):
                value1 += SOBEL_X.item(r+1,c+1) * roi.item(i+r,j+c,1)
                value2 += SOBEL_Y.item(r+1,c+1) * roi.item(i+r,j+c,1)
        value1 = abs(value1)
        value2 = abs(value2)
        if value1>255:
            value1=255
        if value2>255:
            value2=255
        value1/=255
        value2/=255
        green_dx.itemset(i,j,value1)
        green_dy.itemset(i,j,value2)

for i in range(1,roi.shape[0]-1):
    for j in range(1,roi.shape[1]-1):
        value1 = 0
        value2 = 0
        for r in range(-1,2):
            for c in range(-1,2):
                value1 += SOBEL_X.item(r+1,c+1) * roi.item(i+r,j+c,2)
                value2 += SOBEL_Y.item(r+1,c+1) * roi.item(i+r,j+c,2)
        value1 = abs(value1)
        value2 = abs(value2)
        if value1>255:
            value1=255
        if value2>255:
            value2=255
        value1/=255
        value2/=255
        red_dx.itemset(i,j,value1)
        red_dy.itemset(i,j,value2)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        grad_yy.itemset(i,j,red_dy.item(i,j)**2 + green_dy.item(i,j)**2 + blue_dy.item(i,j)**2)
        grad_xx.itemset(i,j,red_dx.item(i,j)**2 + green_dx.item(i,j)**2 + blue_dx.item(i,j)**2)
        grad_yx.itemset(i,j,red_dy.item(i,j)*red_dx.item(i,j) + green_dy.item(i,j)* green_dx.item(i,j) + blue_dy.item(i,j)* blue_dx.item(i,j))
for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        value = 0.5 * math.atan2(2*grad_yx.item(i,j),(grad_xx.item(i,j) - grad_yy.item(i,j)))
        value2 = (red_dx.item(i,j)+green_dx.item(i,j)+blue_dx.item(i,j))//3 + (red_dy.item(i,j)+green_dy.item(i,j)+blue_dy.item(i,j))//3
        Edge_D.itemset(i,j,value)
        Ave_map.itemset(i,j,value2)
        Edge_S.itemset(i,j,math.sqrt(0.5 * ((grad_yy.item(i,j)+ grad_xx.item(i,j)+(grad_xx.item(i,j)-grad_yy.item(i,j)) * math.cos(2*Edge_D.item(i,j)))+2*grad_yx.item(i,j)*math.sin(2*Edge_D.item(i,j)))))

Ave_map= np.abs(Ave_map)
S_map = np.abs(Edge_S)

AVE_MAX = np.max(Ave_map)
D_MAX = np.max(S_map)

Ave_map /= AVE_MAX
S_map /= D_MAX

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        if Ave_map.item(i,j) > 0.2:
            Ave_edge.itemset(i,j,Ave_map.item(i,j))
        if S_map.item(i,j) > 0.2:
            Dizenzo.itemset(i,j,S_map.item(i,j))

# THRESH = 90
# for i in range(roi.shape[0]):
#     for j in range(roi.shape[1]):
#         if abs(blue_dx.item(i,j)) > THRESH:
#             ColorEdge_x.itemset(i,j,0,255)
#         if abs(blue_dy.item(i,j)) > THRESH:
#             ColorEdge_y.itemset(i,j,0,255)
#         if abs(green_dx.item(i,j)) > THRESH:
#             ColorEdge_x.itemset(i,j,1,255)
#         if abs(green_dy.item(i,j)) > THRESH:
#             ColorEdge_y.itemset(i,j,1,255)
#         if abs(red_dx.item(i,j)) > THRESH:
#             ColorEdge_x.itemset(i,j,2,255)
#         if abs(red_dy.item(i,j)) > THRESH:
#             ColorEdge_y.itemset(i,j,2,255)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        ColorEdge_x.itemset(i,j,0,blue_dx.item(i,j))
        ColorEdge_y.itemset(i,j,0,blue_dy.item(i,j))
        ColorEdge_x.itemset(i,j,1,green_dx.item(i,j))
        ColorEdge_y.itemset(i,j,1,green_dy.item(i,j))
        ColorEdge_x.itemset(i,j,2,red_dx.item(i,j))
        ColorEdge_y.itemset(i,j,2,red_dy.item(i,j))

cv.imshow('Canny',edge)
cv.imshow('Di Zenzo',Dizenzo)
cv.imshow('ColorEdge',ColorEdge_x+ColorEdge_y)
cv.imshow('edge_ave',Ave_edge)
cv.waitKey(0)
cv.destroyAllWindows()