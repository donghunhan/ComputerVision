import cv2 as cv
import numpy as np

roi = cv.imread('lenna(gray).jpg')

equalized_roi = np.zeros((roi.shape[0],roi.shape[1],roi.shape[2]),dtype=np.uint8)

g_hist = np.zeros((256),dtype=np.int)

g_hist_norm = np.zeros((256),dtype=np.float)

g_hist_c = np.zeros((256),dtype=np.float)

g_hist_ltable = np.zeros((256),dtype=np.int)

# 히스토그램 계산
for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        g_hist[roi[i,j,0]] += 1

# 히스토그램 정규화
for i in range(256):
    g_hist_norm[i] = g_hist[i] / (roi.shape[0]*roi.shape[1])

# 누적 히스토그램 계산
g_hist_c[0] = g_hist_norm[0]

for i in range(1,256):
    g_hist_c[i] = g_hist_c[i-1] + g_hist_norm[i]

for i in range(256):
    g_hist_ltable[i] = round(g_hist_c[i] * 255)

# 이미지 평활화 수행
for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        equalized_roi[i,j,0] = g_hist_ltable[roi[i,j,0]]
        equalized_roi[i,j,1] = g_hist_ltable[roi[i,j,0]]
        equalized_roi[i,j,2] = g_hist_ltable[roi[i,j,0]]

# 출력
cv.imshow('roi',roi)
cv.imshow('equalized_roi',equalized_roi)
cv.waitKey(0)
cv.destroyAllWindows()