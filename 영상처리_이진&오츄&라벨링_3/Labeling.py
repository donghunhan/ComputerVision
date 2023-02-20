import cv2 as cv
import numpy as np
import queue
import random

# 책에 소개된 라벨링 함수
def flood_fill4(l,j,i,label):
    Q = queue.Queue()
    Q.put((j,i))
    while not Q.empty():
        x, y = Q.get()
        if l.item(x,y) == -1:
            left = right = x
            while l.item(left-1,y) == -1:
                left -=1
            while l.item(right+1,y) == -1:
                right +=1
            # 첫 시작지점부터 왼쪽 오른쪽으로 쭉 이동하여 라벨링 되지않은 부분들을 찾는다.
            for c in range(left,right+1):
                # 왼쪽부터 오른쪽까지 이동하면서 라벨링을 수행한다. (같은 열에 연속된 것들 라벨링)
                l.itemset(c,y,label)
                # 만약 맨 왼쪽에서 아래나 위가 라벨링되어있지 않으면 큐에넣어 다음 반복에 라벨링을 수행한다.
                # 뒤쪽의 조건(and (c == left or l.item(c-1,y-1) != -1))은 불필요한 좌표를 큐에 넣지않기 위함이다. 
                if l.item(c,y-1) == -1 and (c == left or l.item(c-1,y-1) != -1):
                    Q.put((c,y-1))
                if l.item(c,y+1) == -1 and (c == left or l.item(c-1,y+1) != -1):
                    Q.put((c,y+1))
                # 밑의 코드역시 위와 동일한 결과를 보여주지만, 불필요한 좌표들이 큐에 들어가게 됨
                # if l.item(c,y-1) == -1 :
                #     Q.put((c,y-1))
                # if l.item(c,y+1) == -1 :
                #     Q.put((c,y+1))

roi = cv.imread('pic2.jpg')

# 이미지를 흑백으로 바꾸고 이진화 시킨다. T = 127
roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
ret, bin_roi = cv.threshold(roi,127,255,cv.THRESH_BINARY)
# ret, bin_roi = cv.threshold(roi,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)

# 라벨링된 결과를 저장할 행렬을 만든다.
label_img = np.zeros((bin_roi.shape[0],bin_roi.shape[1]),dtype=np.int)

# 책에서 1은 -1 0은 0으로 복사한다고 했음. 여기서는 이진화 된 값인 255와 0으로 구별하여 255이면 -1 나머지는 0으로 복사
# 이미지 밖으로 나가는것을 막기위해 맨 바깥쪽 픽셀영역은 전부 0으로 복사
for i in range(bin_roi.shape[1]):
    for j in range(bin_roi.shape[0]):
        if j == 0 or j == bin_roi.shape[0]-1 or i == 0 or i == bin_roi.shape[1] - 1 :
            label_img.itemset(j,i,0) # 경계 0으로 채우기. 끝을 검사하지 않기위해서
        elif bin_roi.item(j,i) == 255:
            #label_img[j][i] = -1
            label_img.itemset(j,i,-1) # 객체픽셀은 -1로 채움
        else:
            label_img.itemset(j,i,0) # 아니면 0

# label : 라벨링 값
label = 1

# -1인 지점을 찾아서 4방향 연결 알고리즘을 사용
for i in range(1,bin_roi.shape[1]-1):
    for j in range(1,bin_roi.shape[0]-1):
        if label_img.item(j,i) == -1:
            flood_fill4(label_img,j,i,label)
            label+=1


# 라벨링된 결과를 RGB채널의 새로운 이미지로 보여줌(객체별로 다른 색상을 적용) - 책에는 없음
new_img = np.zeros((bin_roi.shape[0],bin_roi.shape[1],3),dtype=np.uint8)

for i in range(bin_roi.shape[1]):
    for j in range(bin_roi.shape[0]):
        if label_img.item(j,i) > 0:
            random.seed(label_img.item(j,i))
            new_img.itemset(j,i,0,random.randint(0,255))
            new_img.itemset(j,i,1,random.randint(0,255))
            new_img.itemset(j,i,2,random.randint(0,255))

print(label)

cv.imshow('bin img',bin_roi)
cv.imshow('label_img',new_img)

cv.waitKey(0)
cv.destroyAllWindows()
