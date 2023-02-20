import sys
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

form_class = uic.loadUiType('window.ui')[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.roi = cv.imread('gray_img.jpg')
        h,w,c = self.roi.shape
        q_Img = QtGui.QImage(self.roi.data,w,h,w*c,QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_Img)
        self.label.setPixmap(pixmap)
        self.roi_gray = self.roi.copy()
        self.new_img = self.roi_gray.copy()

    def btn1_clicked(self): # 팽창
        for i in range(self.roi_gray.shape[0]):
            for j in range(self.roi_gray.shape[1]):
                arr = np.zeros(9)
                index=0
                for r in range(-1,2):
                    for c in range(-1,2):
                        if i+r < 0 or j+c <0 or i+r > self.roi_gray.shape[0]-1 or j+c > self.roi_gray.shape[1]-1:
                            arr.itemset(index,-999)
                        else:
                            arr.itemset(index, self.roi_gray.item(i+r,j+c,0))
                        index+=1
                arr.sort()
                for k in range(3):
                    self.new_img.itemset(i,j,k,arr.item(8))
        self.roi_gray = self.new_img.copy() # 배열의 값 자체 복사하기 위함
        h,w,c = self.roi_gray.shape
        q_Img = QtGui.QImage(self.roi_gray.data,w,h,w*c,QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_Img)
        self.label.setPixmap(pixmap)

    def btn2_clicked(self): # 침식
        for i in range(self.roi_gray.shape[0]):
            for j in range(self.roi_gray.shape[1]):
                arr = np.zeros(9)
                index=0
                for r in range(-1,2):
                    for c in range(-1,2):
                        if i+r < 0 or j+c <0 or i+r > self.roi_gray.shape[0]-1 or j+c > self.roi_gray.shape[1]-1:
                            arr.itemset(index,999)
                        else:
                            arr.itemset(index, self.roi_gray.item(i+r,j+c,0))
                        index+=1
                arr.sort()
                for k in range(3):
                    self.new_img.itemset(i,j,k,arr.item(0))
        self.roi_gray = self.new_img.copy() # 배열의 값 자체 복사하기 위함
        h,w,c = self.roi_gray.shape
        q_Img = QtGui.QImage(self.roi_gray.data,w,h,w*c,QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_Img)
        self.label.setPixmap(pixmap)

    def btn3_clicked(self): # 저장
        cv.imwrite('result.jpg',self.roi_gray)
        print('saved!')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
