import cv2 as cv
import numpy as np

# 이미지 불러오기
roi = cv.imread('lenna.png')

# 원본 이미지와 같은 크기의 빈 이미지 생성
negative_img = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8) 

# 원본이미지를 돌면서 픽셀 하나씩 참조
for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        # OpenCV에서 이미지는 bgr채널로 이루어짐.
        # 이미지 반전은 255에서 원본 픽셀값을 빼주면 적용할 수 있음.
        #value = (roi[i,j,0] + roi[i,j,1] + roi[i,j,2])/3
        #value = (int(roi[i,j,0]) + int(roi[i,j,1]) + int(roi[i,j,2])) / 3
        value = roi[i,j,2] * 0.299 + roi[i,j,1] * 0.587 + roi[i,j,0] * 0.114
        negative_img[i,j,0] = value # b 채널의 픽셀 계산
        negative_img[i,j,1] = value # g 채널의 픽셀 계산
        negative_img[i,j,2] = value # r 채널의 픽셀 계산

cv.imshow('origin', roi) # 원본 이미지 출력
cv.imshow('negative', negative_img) # 반전된 이미지 출력
cv.waitKey(0)
cv.destroyAllWindows() 