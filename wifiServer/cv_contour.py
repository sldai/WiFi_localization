#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import cv2
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as pyplot
img = loadmat('map_data/img.mat')
img=img['img']
img = np.array(img, dtype= np.uint8)
zero = np.zeros(img.shape, dtype = np.uint8)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img[i,j] == 1:
            zero[i, j] = 1

_, contours, _ = cv2.findContours(zero, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for contour_point in contours[1]:
    inter_contour_point = contour_point[0]
    img[inter_contour_point[1], inter_contour_point[0]] = 2
pyplot.imshow(img)
pyplot.show()
