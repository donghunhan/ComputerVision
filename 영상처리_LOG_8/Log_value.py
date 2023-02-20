import cv2 as cv
import numpy as np
import math

input_arr  = np.array([
    [0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,1,0],
    [0,1,2,0,0,0,1,0],
    [0,1,3,1,0,0,2,0],
    [0,1,3,1,0,0,2,0],
    [0,1,2,3,4,4,3,0],
    [0,0,0,0,1,3,1,0],
    [0,0,0,0,0,0,0,0]
    ])

SIGMA = 0.5

def gauss(y,x,sigma):
    value = math.exp(-(x**2+y**2)/(2*sigma**2))
    return value/(2*math.pi*sigma**2)

LogSize = (int)(6*SIGMA)
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

gap_image = np.zeros((input_arr.shape[0],input_arr.shape[1]),dtype=np.uint8)
# for i in range(gap_image.shape[0]):
#     for j in range(gap_image.shape[1]):
#         gap_image.itemset(i,j,255)
Log_image = np.zeros((input_arr.shape[0],input_arr.shape[1]))
maxi = 0
for i in range(input_arr.shape[0]):
    for j in range(input_arr.shape[1]):
        G = 0
        for r in range(-(LogSize//2), (LogSize//2)+1):
            for c in range(-(LogSize//2), (LogSize//2)+1):
                y = i+r
                x = j+c
                if y >= 0 and x >= 0 and y < gap_image.shape[0] and x < gap_image.shape[1]:
                    pixelData = input_arr.item(y,x)
                    G += pixelData * LogFilter.item(r + (LogSize//2), c + (LogSize//2))
        if G > maxi:
            maxi = G
        Log_image.itemset(i,j,G)
for i in range (1,gap_image.shape[0]-1):
    for j in range (1,gap_image.shape[1]-1):
        gap = 0
        count = 0
        zero_count = 0
        if (Log_image.item(i-1,j) > 0 and  Log_image.item(i+1,j) < 0) or (Log_image.item(i-1,j) < 0 and  Log_image.item(i+1,j) > 0):
            zero_count += 1
            gap = math.fabs(Log_image.item(i-1,j-1)-Log_image.item(i+1,j+1))
            if gap > 1.0:
                count += 1
            # 남-북 영교차가 일어나는지 보고, 그 차이 값이 임계값(최댓값*0.05)보다 큰지 확인 
            # 크면 영교차 횟수 증가
        for k in range(-1,2):
            if ( Log_image.item(i+k,j-1) > 0 and  Log_image.item(i-k,j+1) < 0) or ( Log_image.item(i+k,j-1) < 0 and  Log_image.item(i-k,j+1) > 0):
                zero_count += 1
                gap = math.fabs(Log_image.item(i-1,j-1)-Log_image.item(i+1,j+1))
                if gap > 1.0:
                    count += 1
            # 북동-남서, 북서-남동, 동-서 방향으로 영교차가 일어나는지 확인.
            # 일어나면 횟수 증가
        if zero_count > 2 and zero_count == count:
            gap_image.itemset(i,j,1)
            # 영교차 횟수가 2회 이상 일어나고, 부호가 다른 쌍의 값 차이가 임계값을 넘으면 엣지로 표시
        else :
            gap_image.itemset(i,j,0)
            # 아니면 흰색으로 표시


for i in range(gap_image.shape[0]):
    for j in range(gap_image.shape[1]):
        print('{0:3d} '.format(gap_image.item(i,j)),end='')
    print()

for i in range(gap_image.shape[0]):
    for j in range(gap_image.shape[1]):
        print('{0:5.4f} '.format(Log_image.item(i,j)),end='')
    print()