import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('scene_dissolve')

cv.createTrackbar('alpha','scene_dissolve',0,100,nothing)

cv.setTrackbarPos('alpha','scene_dissolve',0)

# 두 영상을 불러옴
roi1 = cv.imread('picture3.jpg')
roi2 = cv.imread('picture4.jpg')

# openCV를 사용하여 크기를 일치시킴
roi1_resized = cv.resize(roi1,dsize=(640,480),interpolation=cv.INTER_LINEAR)
roi2_resized = cv.resize(roi2,dsize=(640,480),interpolation=cv.INTER_LINEAR)

output = np.zeros((480,640,3),dtype=np.uint8)

while True:
    alpha = cv.getTrackbarPos('alpha','scene_dissolve')/100
    print('running...')
    for k in range(3):
        for j in range(640):
            for i in range(480):
                value = int(roi1_resized.item(i,j,k)* alpha + (1-alpha)*roi2_resized.item(i,j,k))
                output.itemset(i,j,k,value) # output[i,j,k] = value

    cv.imshow('scene_dissolve',output)

    if cv.waitKey(1) & 0xFF == 27: # ESC를 누르면 종료
        break

cv.destroyAllWindows()