#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, Matern, ConstantKernel, RBF, RationalQuadratic
from sklearn.model_selection import train_test_split
from mpl_toolkits.mplot3d import Axes3D

dataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static.csv", dtype=float, delimiter=',')[:,1:]
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-07-16 19_23_44.csv", dtype=float, delimiter=',')
lenArray = min(len(dataAll), len(data))
inputNum = 2
for i in range(10):

    for j in range(lenArray):
        if dataAll[j,i+2]==-100:
            data[j,i+3]=-100
np.savetxt("E:/WiFi/实验室6楼/wifiData/实验/2018-07-16 19_23_44 re.csv", np.array(data), fmt='%f', delimiter=',', newline='\r\n')