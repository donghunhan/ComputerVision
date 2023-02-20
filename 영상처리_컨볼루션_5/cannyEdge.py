import cv2 as cv
import numpy as np
import math
import queue

SIGMA = 1.0
LOW_T = 0.25 * 255
HIGH_T = 0.1 * 255

def gauss(y,x,sigma):
    value = math.exp(-(x**2+y**2)/(2*sigma**2))
    return value/(2*math.pi*sigma**2)

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

DIRECTION_LIST = [(-1,0,1,0),(-1,1,1,-1),(0,1,0,-1),(-1,-1,1,1)]
yx_list = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

FILTER_SIZE = int(SIGMA*6)
if FILTER_SIZE % 2 == 0:
    FILTER_SIZE += 1
print('filtersize : ',FILTER_SIZE)
ROI = cv.imread('1.jpg')
ROI_GRAY = cv.cvtColor(ROI,cv.COLOR_BGR2GRAY)

map_dy = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))
map_dx = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))

mag_map = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))
dir_map = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]),dtype=np.uint8)

gaussblurred = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))

edge_map = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))
visited = np.zeros((ROI_GRAY.shape[0],ROI_GRAY.shape[1]))

gauss_filter = np.zeros((FILTER_SIZE,FILTER_SIZE))
SIZE = int(FILTER_SIZE//2)

# 가우시안 필터를 구함
for x in range(FILTER_SIZE):
    for y in range(FILTER_SIZE):
        # a = math.exp(-(((y-(FILTER_SIZE//2))**2) + ((x-(FILTER_SIZE//2))**2))/2*SIGMA**2)
        # b = 1/(2* math.pi * SIGMA**2)
        gauss_value = gauss(x-SIZE,y-SIZE,SIGMA)
        gauss_filter.itemset(x,y,gauss_value)
print('gaussian filter has been created.')
# 가우시안 필터를 적용시켜 노이즈 제거
for i in range(SIZE,ROI_GRAY.shape[0]-SIZE):
    for j in range(SIZE,ROI_GRAY.shape[1]-SIZE):
        value = 0.0
        for r in range(-SIZE,SIZE+1):
            for c in range(-SIZE,SIZE+1):
                value += gauss_filter.item(r+SIZE,c+SIZE) * ROI_GRAY.item(i+r,j+c)
        gaussblurred.itemset(i,j,value)
print('blurred_img has been created.')
# 소벨 필터를 사용하여 엣지검출
for i in range(1,gaussblurred.shape[0]-1):
    for j in range(1,gaussblurred.shape[1]-1):
        value1 = 0.0
        value2 = 0.0
        for r in range(-1,2):
            for c in range(-1,2):
                value1 += SOBEL_X.item(r+1,c+1) * gaussblurred.item(i+r,j+c)
                value2 += SOBEL_Y.item(r+1,c+1) * gaussblurred.item(i+r,j+c)
        map_dx.itemset(i,j,value1)
        map_dy.itemset(i,j,value2)
print('edge has been created.')
# x축과 y축으로 검출된 엣지를 사용하여 각 픽셀에서의 그래디언트 크기와 방향을 구함
for i in range(gaussblurred.shape[0]):
    for j in range(gaussblurred.shape[1]):
        magnitude = math.sqrt(map_dx.item(i,j)**2 +map_dy.item(i,j)**2)
        direction = math.atan2(map_dy.item(i,j),map_dx.item(i,j)) + 90 # 엣지방향은 그래디언트 방향에 수직
        direction = (direction/360)*8
        mag_map.itemset(i,j,magnitude)
        dir_map.itemset(i,j,direction)
print('gradient has been computed.')
# 비최대억제를 통해 가짜 엣지를 제거함
'''
비최대 억제의 경우 자신 주변의 픽셀(엣지 방향에 따라 참조픽셀 위치가 다름)들 보다 
그래디언트 크기가 작으면 엣지에서 제외함.
'''
for i in range(1,gaussblurred.shape[0]-1):
    for j in range(1,gaussblurred.shape[1]-1):
        y1,x1,y2,x2 = DIRECTION_LIST[int(dir_map.item(i,j))%4]
        y1 += i
        x1 += j
        y2 += i
        x2 += j
        if mag_map.item(i,j) <= mag_map.item(y1,x1) or mag_map.item(i,j) <= mag_map.item(y2,x2):
            mag_map.itemset(i,j,0)
print('fake edges have been deleted.')

# def follow_edge(y,x):
#     visited.itemset(y,x,1)
#     edge_map.itemset(y,x,255)
#     for y1,x1 in yx_list:
#         if mag_map.item(y1+y,x1+x)>LOW_T and visited.item(y1+y,x1+x) == 0:
#             follow_edge(y1+y,x1+x)

# 이력임계값을 사용하여 엣지 추정
'''
이력임계값은 우선 엣지일 확률이 높은(임계값T_high보다 큰)곳에서 엣지추적을 시작함.
그 주변 엣지들을 대상으로 픽셀이 T_low보다 큰값을 가지면 엣지로 간주.
'''
Q = queue.Queue()
for i in range(1,edge_map.shape[0]-1):
    for j in range(1,edge_map.shape[1]-1):
        if mag_map.item(i,j) > HIGH_T and visited.item(i,j) == 0:
            # follow_edge(i,j)
            Q.put((i,j))
            while not Q.empty():
                y, x = Q.get()
                visited.itemset(y,x,1)
                edge_map.itemset(y,x,255)
                for y1,x1 in yx_list:
                    if mag_map.item(y1+y,x1+x)>LOW_T and visited.item(y1+y,x1+x) == 0:
                        visited.itemset(y1+y,x1+x,1)
                        edge_map.itemset(y1+y,x1+x,255)
                        Q.put((y+y1,x+x1))
print('found edges.')

cv.imshow('canny_edge',edge_map)
cv.waitKey(0)
cv.destroyAllWindows()
