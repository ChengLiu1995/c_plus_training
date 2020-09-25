# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:30:42 2020

@author: 73766
"""
import matplotlib.pyplot as plt 
import numpy as np
import scipy.signal as signal 
import math
import cv2


img = cv2.imread("../imgs/2020.png")

img = np.mean(np.float32(img), axis=2)

suanzi_x = np.array([[1, 0, -1],
                    [ 2, 0, -2],
                    [ 1, 0, -1]])

suanzi_y = np.array([[ 1, 2, 1],
                     [ 0, 0, 0],
                     [ -1, -2, -1]])

grad_x = signal.convolve2d(img,suanzi_x,mode="same")
grad_y = signal.convolve2d(img,suanzi_y,mode="same")

Ixx = grad_x*grad_x
Iyy = grad_y*grad_y
Ixy = grad_x*grad_y

#加权的W，这里权重都取1
Ixx_w =cv2.blur(Ixx,(3,3)) 
Iyy_w =cv2.blur(Iyy,(3,3))
Ixy_w =cv2.blur(Ixy,(3,3))

H = img.shape[0]
L = img.shape[1]
corners = np.zeros((H,L),dtype=np.float32)

for i in range(H):
    for j in range(L):
        ixx = Ixx_w[i,j]
        iyy = Iyy_w[i,j]
        ixy = Ixy_w[i,j]
        trace_ = ixx + iyy
        det = ixx * iyy - ixy*ixy
        corners[i][j] = det - 0.05*trace_**2
plt.figure()
plt.imshow(img,"gray") # 显示图片
plt.axis('off') # 不显示坐标轴
plt.show()

plt.figure()
plt.imshow(corners,"gray") # 显示图片
plt.axis('off') # 不显示坐标轴
plt.show()
