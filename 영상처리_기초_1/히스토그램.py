import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

roi = cv.imread('lenna.png')

r_hist = np.zeros((256),dtype=np.int)
g_hist = np.zeros((256),dtype=np.int)
b_hist = np.zeros((256),dtype=np.int)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        b_hist[roi[i,j,0]] += 1
        g_hist[roi[i,j,1]] += 1
        r_hist[roi[i,j,2]] += 1

plt.subplot(1,2,1)
b,g,r = cv.split(roi)
roi_rgb = cv.merge([r,g,b])
plt.imshow(roi_rgb)
plt.subplot(1,2,2)
plt.plot(b_hist, color='b')
plt.plot(g_hist, color='g')
plt.plot(r_hist, color='r')
plt.show()