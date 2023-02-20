import numpy as np
import math

SIGMA = 1.0

def gauss(y,x,sigma):
    value = math.exp(-(x**2+y**2)/(2*sigma**2))
    return value/(2*math.pi*sigma**2)

LogSize = 3
LogFilter = np.zeros((LogSize,LogSize))
for i in range(LogSize):
    for j in range(LogSize):
        gauss_value = gauss(i-(LogSize//2),j-(LogSize//2),SIGMA)
        LogFilter.itemset(i,j,gauss_value)

for i in range(LogFilter.shape[0]):
    for j in range(LogFilter.shape[1]):
        print('{0:0.4f} '.format(LogFilter.item(i,j)),end='')
    print()
