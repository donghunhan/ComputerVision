import cv2 as cv
import numpy as np

mask = np.array([
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1],
    [0,1,1,1,1,1,0],
    [0,0,1,1,1,0,0],
])

T1 = 10 # 책에서는 제시되지 않아서 임의로 설정
T2 = 18.5 # 마스크 넓이 * 0.5
Q = 27.75 # 마스크 넓이 * 0.75

origin = cv.imread('pattern.png')
roi = cv.imread('pattern.png',cv.IMREAD_GRAYSCALE)
C_map = np.zeros((roi.shape[0],roi.shape[1]),np.uint8)
corner_map = origin.copy()

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        usan_area = 0
        for r in range(-3,4):
            for c in range(-3,4):
                y = i + r
                x = j + c
                if r == 0 and c == 0:
                    continue
                if (y >= 0 and y< roi.shape[0] and x >=0 and x< roi.shape[1]) and mask.item(r+3,c+3) == 1:
                    if abs(roi.item(y,x) - roi.item(i,j)) <= T1: # 기준점과의 차이가 10보다 작으면 유사한 픽셀. 즉, 우산이다.
                        usan_area += 1 # 우산 값을 늘린다.
        if usan_area <= T2: # 우산의 수가 마스크의 넓이의 50퍼 이하면 코너로 본다.
            C_map.itemset(i,j,Q-usan_area) # 특징 가능성 값은 q - usan_area 이다.

cv.imshow('C_map',C_map)

C_map = cv.dilate(C_map,None) # 코너를 더 잘 보이게 하기위해 모폴로지로 명암값을 전체적으로 끌어올림(팽창 연산)
corner_map[C_map >= 0.9 * C_map.max()] = [0,0,255] # numpy인덱싱으로 가장 큰 가능성값의 90퍼센트 까지 일치하는 점 부분만 붉은색으로 표시 

cv.imshow('corner',corner_map)
cv.waitKey(0)
cv.destroyAllWindows()