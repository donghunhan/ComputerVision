import cv2 as cv
import numpy as np
import math

def gauss(y,x,sigma):
    value = math.exp(-(x**2+y**2)/(2*sigma**2))
    return value/(2*math.pi*sigma**2)

gauss_filter = np.zeros((5,5))

for x in range(5):
    for y in range(5):
        # a = math.exp(-(((y-(FILTER_SIZE//2))**2) + ((x-(FILTER_SIZE//2))**2))/2*SIGMA**2)
        # b = 1/(2* math.pi * SIGMA**2)
        gauss_value = gauss(x-2,y-2,0.50715)
        gauss_filter.itemset(x,y,gauss_value)

print(gauss_filter)