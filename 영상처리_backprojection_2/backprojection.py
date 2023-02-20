import cv2 as cv
import numpy as np

roi = cv.imread('model.png')
hsv_roi = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv_target = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    M = cv.calcHist([hsv_roi],[0, 1], None, [180, 256], [0, 180, 0, 256] )
    I = cv.calcHist([hsv_target],[0, 1], None, [180, 256], [0, 180, 0, 256] )

    R = M/(I+1)

    h,s,v = cv.split(hsv_target)
    B = R[h.ravel(), s.ravel()]
    B = np.minimum(B, 1)
    B = B.reshape(hsv_target.shape[:2])

    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    cv.filter2D(B, -1, disc, B)
    B = np.uint8(B)
    cv.normalize(B, B, 0, 255, cv.NORM_MINMAX)

    ret,thresh = cv.threshold(B,20,255,0)

    thresh = cv.merge((thresh,thresh,thresh))
    res = cv.bitwise_and(frame,thresh)


    cv.imshow("result1", B)
    cv.imshow("result2", res)

    k= cv.waitKey(1)
    if k == 27:
        break
cap.release()

cv.destroyAllWindows()

# target = cv.imread('target.png')
# hsv_target = cv.cvtColor(target,cv.COLOR_BGR2HSV)

# M = cv.calcHist([hsv_roi],[0, 1], None, [180, 256], [0, 180, 0, 256] )
# I = cv.calcHist([hsv_target],[0, 1], None, [180, 256], [0, 180, 0, 256] )

# R = M/(I+1)


# h,s,v = cv.split(hsv_target)
# B = R[h.ravel(), s.ravel()]
# B = np.minimum(B, 1)
# B = B.reshape(hsv_target.shape[:2])


# disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
# cv.filter2D(B, -1, disc, B)
# B = np.uint8(B)
# cv.normalize(B, B, 0, 255, cv.NORM_MINMAX)

# ret,thresh = cv.threshold(B,20,255,0)

# thresh = cv.merge((thresh,thresh,thresh))
# res = cv.bitwise_and(target,thresh)


# cv.imshow("result1", B)
# cv.imshow("result2", res)
# cv.waitKey(0)