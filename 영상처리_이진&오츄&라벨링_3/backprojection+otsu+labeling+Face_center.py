import cv2 as cv
import numpy as np
import math
import queue
import random

# 모델 이미지와 HSV공간으로 변환한 모델 이미지
roi = cv.imread('model.png')
hsv_roi = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

# 타겟 이미지와 HSV공간으로 변환한 타겟 이미지
target = cv.imread('4.jpg')
hsv_target = cv.cvtColor(target,cv.COLOR_BGR2HSV)
# 책에서 q단계로 줄인 2차원 히스토그램을 만든다. 여기서는 64를 사용하였다.
scale = 16

# 각각 q단계인 모델 HS히스토그램과 타겟 HS히스토그램을 만듬
model_hist = np.zeros((scale,scale))
# target_hist = np.zeros((scale,scale))

# 알고리즘 2-2를 사용하여 정규화된 히스토그램을 만든다.(모델만 만듬.)
for i in range(hsv_roi.shape[1]):
    for j in range(hsv_roi.shape[0]):
        model_hist[math.trunc(hsv_roi.item(j,i,0)/180*(scale-1)),math.trunc(hsv_roi.item(j,i,1)*(scale-1)/255)]+=1
for i in range(scale):
    for j in range(scale):
        norm_model_hist = model_hist/(hsv_roi.shape[0] * hsv_roi.shape[1])
norm_model_hist /= np.max(norm_model_hist) # 0~1 사이의 값으로 정규화.

# 타겟이미지와 같은 크기를 가지는 빈 이미지를 만든다.
backP_img = np.zeros((target.shape[0],target.shape[1]),np.float64)
backP_img_u = np.zeros((target.shape[0],target.shape[1]),np.uint8)

# 타겟 이미지의 픽셀값을 양자화 하여 모델 히스토그램으로 이동하여 나오는 색상값으로 역투영을 수행한다.
for i in range(hsv_target.shape[1]):
    for j in range(hsv_target.shape[0]):
        backP_img[j,i] = norm_model_hist[math.trunc(hsv_target.item(j,i,0)/180*(scale-1)),math.trunc(hsv_target.item(j,i,1)/255*(scale-1))]
        backP_img_u[j,i] = backP_img[j,i] * 255

gray_hist = np.zeros(256)
# 정규화된 히스토그램 생성
norm_hist = np.zeros(256,dtype=np.float)

# 기본 히스토그램을 구한다.
for i in range(backP_img_u.shape[1]):
    for j in range(backP_img_u.shape[0]):
        gray_hist[backP_img_u.item(j,i)]+=1
# 정규화 시켜서 저장한다.
for i in range(256):
    norm_hist[i] = gray_hist[i] / (backP_img_u.shape[0]*backP_img_u.shape[1])

vwlist = []
#vwlist2 = [] #without weight

for i in range(256): #T값을 결정하기위해서 1부터~255단계까지 바꾸어 나간다
    w0 = 0.0
    w1 = 0.0
    u0 = 0.0
    u1 = 0.0
    v0 = 0.0
    v1 = 0.0
    for j in range(i):
        w0 += norm_hist[j] #T가 1이라면  정규화된 값을 넣고
    for j in range(i+1,256):
        w1 += norm_hist[j] # 나머지값(2부터255까지 누적값 더하기)을 w1에넣고
        
    if w0 != 0:
        for j in range(i):
            u0 += j*norm_hist[j]
        u0 /= w0
        for j in range(i):
            v0 += norm_hist[j]*(j-u0)**2
        v0 /= w0

    if w1 != 0:
        for j in range(i+1,256):
            u1 += j*norm_hist[j]
        u1 /= w1
        for j in range(i+1,256):
            v1 += norm_hist[j]*(j-u1)**2
        v1 /= w1

    v_within = w0 * v0 + w1 * v1
    #v_within2 = v0 + v1 #without weight
    vwlist.append(v_within)
    #vwlist2.append(v_within2) #without weight
    #if v_within < best:
        #best = v_within
        #best_t = i
        #T_max[0] = i
        #T_max[1] = v_within

#print(T_max)
#print(best, best_t)

#print(vwlist)
t_argmin = np.argmin(vwlist)
print(t_argmin, vwlist[t_argmin])

binary = np.zeros((backP_img_u.shape[0],backP_img_u.shape[1]),dtype=np.uint8)

for i in range(backP_img_u.shape[0]):
    for j in range(backP_img_u.shape[1]):
        if backP_img_u[i,j] >= t_argmin:
            binary[i,j] = 255
        else:
            binary[i,j] = 0

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

# 라벨링된 결과를 저장할 행렬을 만든다.
label_img = np.zeros((binary.shape[0],binary.shape[1]),dtype=np.int)

# 책에서 1은 -1 0은 0으로 복사한다고 했음. 여기서는 이진화 된 값인 255와 0으로 구별하여 255이면 -1 나머지는 0으로 복사
# 이미지 밖으로 나가는것을 막기위해 맨 바깥쪽 픽셀영역은 전부 0으로 복사
for i in range(binary.shape[1]):
    for j in range(binary.shape[0]):
        if j == 0 or j == binary.shape[0]-1 or i == 0 or i == binary.shape[1] - 1 :
            label_img.itemset(j,i,0) # 경계 0으로 채우기. 끝을 검사하지 않기위해서
        elif binary.item(j,i) == 255:
            #label_img[j][i] = -1
            label_img.itemset(j,i,-1) # 객체픽셀은 -1로 채움
        else:
            label_img.itemset(j,i,0) # 아니면 0

# label : 라벨링 값
label = 1

# -1인 지점을 찾아서 4방향 연결 알고리즘을 사용
for i in range(1,binary.shape[1]-1):
    for j in range(1,binary.shape[0]-1):
        if label_img.item(j,i) == -1:
            flood_fill4(label_img,j,i,label)
            label+=1


# 라벨링된 결과를 RGB채널의 새로운 이미지로 보여줌(객체별로 다른 색상을 적용) - 책에는 없음
new_img = np.zeros((binary.shape[0],binary.shape[1],3),dtype=np.uint8)

for i in range(binary.shape[1]):
    for j in range(binary.shape[0]):
        if label_img.item(j,i) > 0:
            random.seed(label_img.item(j,i))
            new_img.itemset(j,i,0,random.randint(0,255))
            new_img.itemset(j,i,1,random.randint(0,255))
            new_img.itemset(j,i,2,random.randint(0,255))

print(label)

bins = np.zeros((label))
for i in range(label_img.shape[0]):
    for j in range(label_img.shape[1]):
        if label_img.item(i,j) > 0: # 배경은 무시한다.
            bins[label_img.item(i,j)]+=1 # 각 라벨별 빈도수 계산
print('face label: ',max(bins))
face = max(np.where(bins==max(bins))) # 가장 많은 빈도수의 라벨을 얼굴이라고 판단.
face_index = np.where(label_img==face) # 라벨 값이 얼굴 라벨값인 것의 위치를 모두 구함.

'''
face_index는 튜플 형식을 지닌다.
첫번째 원소는 행들의 집합. 두번째 원소는 열들의 집합이다.
'''

pt1_y = min(face_index[0]) # 얼굴 좌측상단 행값. 행값들중 최솟값
pt1_x = min(face_index[1]) # 얼굴 좌측상단 열값. 열값들중 최솟값
pt2_y = max(face_index[0]) # 얼굴 우측하단 행값. 행값들중 최댓값
pt2_x = max(face_index[1]) # 얼굴 우측하단 열값. 열값들중 최댓값
face_pos = ((pt1_x+pt2_x)//2,(pt1_y+pt2_y)//2) # 얼굴 중심 계산

cv.rectangle(new_img,(pt1_x,pt1_y),(pt2_x,pt2_y),(255,255,255),2) # 얼굴 영역 표시 그리기 
cv.circle(new_img,face_pos,5,(0,0,255),cv.FILLED) # 얼굴 중심 표시 그리기

cv.imshow('label_img',new_img)

# 이미지를 출력한다. imshow함수는 입력되는 배열의 값이 소수일 경우 [0.0, 1.0]의 범위를 [0, 255]에 매핑하여 변환해 출력해준다.
cv.imshow('img',backP_img)
cv.imshow('binary img',binary)
cv.waitKey(0)
cv.destroyAllWindows()