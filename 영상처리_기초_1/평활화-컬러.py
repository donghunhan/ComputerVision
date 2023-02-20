import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

roi = cv.imread('lenna.png')

equalized_roi = np.zeros((roi.shape[0],roi.shape[1],roi.shape[2]),dtype=np.uint8)

r_hist = np.zeros((256),dtype=np.int)
g_hist = np.zeros((256),dtype=np.int)
b_hist = np.zeros((256),dtype=np.int)

r_hist_norm = np.zeros((256),dtype=np.float)
g_hist_norm = np.zeros((256),dtype=np.float)
b_hist_norm = np.zeros((256),dtype=np.float)

r_hist_c = np.zeros((256),dtype=np.float)
g_hist_c = np.zeros((256),dtype=np.float)
b_hist_c = np.zeros((256),dtype=np.float)

r_hist_ltable = np.zeros((256),dtype=np.int)
g_hist_ltable = np.zeros((256),dtype=np.int)
b_hist_ltable = np.zeros((256),dtype=np.int)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        b_hist[roi[i,j,0]] += 1
        g_hist[roi[i,j,1]] += 1
        r_hist[roi[i,j,2]] += 1

for i in range(256):
    r_hist_norm[i] = r_hist[i] / (roi.shape[0]*roi.shape[1])
    g_hist_norm[i] = g_hist[i] / (roi.shape[0]*roi.shape[1])
    b_hist_norm[i] = b_hist[i] / (roi.shape[0]*roi.shape[1])

r_hist_c[0] = r_hist_norm[0]
g_hist_c[0] = g_hist_norm[0]
b_hist_c[0] = b_hist_norm[0]

for i in range(1,256):
    r_hist_c[i] = r_hist_c[i-1] + r_hist_norm[i]
    g_hist_c[i] = g_hist_c[i-1] + g_hist_norm[i]
    b_hist_c[i] = b_hist_c[i-1] + b_hist_norm[i]

for i in range(256):
    r_hist_ltable[i] = round(r_hist_c[i] * 255)
    g_hist_ltable[i] = round(g_hist_c[i] * 255)
    b_hist_ltable[i] = round(b_hist_c[i] * 255)

for i in range(roi.shape[0]):
    for j in range(roi.shape[1]):
        equalized_roi[i,j,2] = r_hist_ltable[roi[i,j,2]]
        equalized_roi[i,j,1] = g_hist_ltable[roi[i,j,1]]
        equalized_roi[i,j,0] = b_hist_ltable[roi[i,j,0]]

plt.subplot(1,2,1)
b,g,r = cv.split(roi)
roi_rgb = cv.merge([r,g,b])
plt.imshow(roi_rgb)
plt.subplot(1,2,2)
b,g,r = cv.split(equalized_roi)
roi_rgb2 = cv.merge([r,g,b])
plt.imshow(roi_rgb2)
plt.show()