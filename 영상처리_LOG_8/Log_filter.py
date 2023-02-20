import numpy as np
import math

SIGMA = 2.0

def gauss(y,x,sigma):
    value = math.exp(-(x**2+y**2)/(2*sigma**2))
    return value/(2*math.pi*sigma**2)

LogSize = (int)(6*SIGMA)
ab = 0
if LogSize%2==0:
    LogSize += 1
LogFilter = np.zeros((LogSize,LogSize))
for x in range(LogSize):
    for y in range(LogSize):
        gauss_value = gauss(x-(LogSize//2),y-(LogSize//2),SIGMA)
        Logvalue = ((x-(LogSize//2))**2+(y-(LogSize//2))**2 - 2*SIGMA**2)/SIGMA**4
        LogFilter.itemset(x,y,gauss_value*Logvalue)

for i in range(LogFilter.shape[0]):
    for j in range(LogFilter.shape[1]):
        print('{0:0.4f} '.format(LogFilter.item(i,j)),end='')
    print()