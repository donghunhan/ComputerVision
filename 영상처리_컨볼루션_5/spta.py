import cv2 as cv
import numpy as np

roi = cv.imread('1.jpg')

gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)

edge = cv.Canny(gray,50,150)
labeled = np.zeros((edge.shape[0],edge.shape[1]))
edge_out = edge.copy()
wrong_edge = edge.copy()

for i in range(1,edge.shape[0]-1):
    for j in range(1,edge.shape[1]-1):
        n0 = edge_out.item(i,j+1) == 255
        n1 = edge_out.item(i-1,j+1) == 255
        n2 = edge_out.item(i-1,j) == 255
        n3 = edge_out.item(i-1,j-1) == 255
        n4 = edge_out.item(i,j-1) == 255
        n5 = edge_out.item(i+1,j-1) == 255
        n6 = edge_out.item(i+1,j) == 255
        n7 = edge_out.item(i+1,j+1) == 255
        if edge_out.item(i,j) == 255 and (
            (not n0 and(n4 and (n5 or n6 or n2 or n3) and (n6 or not n1) and (n2 or not n1)))
            or (not n4 and (n0 and (n1 or n2 or n6 or n1) and (n2 or not n3) and (n6 or not n5))) 
            or (not n2 and (n5 and (n1 or n0 or n4 or n5) and (n0 or not n1) and (n4 or not n3)))
            or (not n6 and (n2 and (n3 or n4 or n0 or n1) and (n4 or not n5) and (n0 or not n1)))
            ):
            edge_out.itemset(i,j,0)
        else:
            labeled.itemset(i,j,1)

cv.imshow('edge',edge_out)
cv.imshow('edge_origin',edge)
cv.waitKey(0)
cv.destroyAllWindows()
