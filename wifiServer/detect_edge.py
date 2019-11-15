#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

def detect_edge(map_array):
    edge_map = cv2.Canny(map_array,0,0)
    return edge_map

# def CannyThreshold(lowThreshold):
#     # detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
#     detected_edges = cv2.Canny(gray, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
#     dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
#     cv2.imshow('canny demo', dst)

if __name__ == '__main__':
    region_group = np.load('map_data/region_group.npy')
    map_data = cv2.imread('map_data/contour.jpg',0)

    plt.imshow(detect_edge(region_group))
    plt.show()
    # lowThreshold = 0
    # max_lowThreshold = 100
    # ratio = 3
    # kernel_size = 3
    #
    # img = cv2.imread('map_data/contour.jpg')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # cv2.namedWindow('canny demo')
    #
    # cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)
    #
    # CannyThreshold(0)  # initialization
    # if cv2.waitKey(0) == 27:
    #     cv2.destroyAllWindows()






