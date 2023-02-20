import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

roi = cv.imread('pic3.jpg')
# Opencv에서 imread함수를 사용하면 흑백이미지여도, rgb 3채널로 입력된다.
gray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)
# 흑백으로 바꿔서 채널을 하나로 줄인다.
binary = np.zeros((gray.shape[0],gray.shape[1]),dtype=np.uint8)

# roi[0,0,0] # b 0,0
for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        if (gray[i][j] >= 127):
            binary[i][j] = 255
        else:
            binary[i][j] = 0


plt.subplot(1,3,1)
b,g,r = cv.split(roi)
roi_rgb = cv.merge([r,g,b])
plt.imshow(roi_rgb)
#plt.imshow(negative_img)
plt.subplot(1,3,2)
plt.imshow(gray, cmap='gray')
plt.subplot(1,3,3)
plt.imshow(binary, cmap='gray')
plt.show()