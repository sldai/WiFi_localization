#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.externals import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, Matern, ConstantKernel, RBF, RationalQuadratic
from sklearn.model_selection import train_test_split
from mpl_toolkits.mplot3d import Axes3D
from restore import Recover
from sklearn.preprocessing import StandardScaler
from outlierInGP import DetectOutlier

data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/complete.csv", dtype=float, delimiter=',')[::1]
data_add = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static.csv", dtype=float, delimiter=',')[24:1276]
data = np.row_stack((data, data_add))
def fingerprint(X, y, grid):
    kernel = 2.0 * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1.0)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    scaler = StandardScaler().fit(X)
    gpr.fit(scaler.transform(X), y)
    y_gpr, y_std = gpr.predict(scaler.transform(grid), return_std=True)

    return np.column_stack((grid, y_gpr, y_std))

# left = 0
# right = 2
# top = 23
# bot = 4.7
left = 16
right = 39
top = 7
bot = 0

resolution = 0.1

grid = []
X, Y = np.meshgrid(np.arange(left, right, resolution), np.arange(bot, top, resolution))
for x in np.arange(left, right, resolution):
    for y in np.arange(bot, top, resolution):
        grid.append([x,y])
grid = np.array(grid)

fg_map = fingerprint(data[:,:2], data[:,1+12], grid)

Z = np.zeros(X.shape)
for i in range(len(fg_map)):
    Z[int(round((fg_map[i,1]-bot)/resolution)), int(round((fg_map[i,0]-left)/resolution))] = fg_map[i,2]

np.savetxt("subarea_3D/X3.csv",
           X, fmt='%f',
           delimiter=',', newline='\r\n')
np.savetxt("subarea_3D/Y3.csv",
           Y, fmt='%f',
           delimiter=',', newline='\r\n')
np.savetxt("subarea_3D/Z3.csv",
           Z, fmt='%f',
           delimiter=',', newline='\r\n')