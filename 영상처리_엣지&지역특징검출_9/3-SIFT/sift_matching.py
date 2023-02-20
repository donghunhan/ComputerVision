import numpy as np
import cv2
from matplotlib import pyplot as plt
img1 = cv2.imread('api2.jpg',0)
img2 = cv2.imread('room.jpg',0)

sift = cv2.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

print(len(kp1),len(des1))
print(len(kp2),len(des2))

bf = cv2.BFMatcher()

matches = bf.match(des1,des2)

print(len(matches))

sorted_matches = sorted(matches, key = lambda x : x.distance)
res = cv2.drawMatches(img1, kp1, img2, kp2, sorted_matches[:30], None, flags = 2)

plt.imshow(res),plt.show()