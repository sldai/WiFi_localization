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


def fingerprint(X, y, grid):
    kernel = 2.0 * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1.0)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    scaler = StandardScaler().fit(X)
    gpr.fit(scaler.transform(X), y)
    y_gpr, y_std = gpr.predict(scaler.transform(grid), return_std=True)

    return np.column_stack((grid, y_gpr, y_std))

data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/complete.csv", dtype=float, delimiter=',')[::1]
data_add = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static.csv", dtype=float, delimiter=',')[24:1276]
data = np.row_stack((data, data_add))
data = data[::4]
X = data[:,:2]
y = data[:,1+12]
grid = []
resolution = 0.05
costmap = np.loadtxt("heatmap/costmap.csv", dtype=float, delimiter=',')
height, width = costmap.shape
costmap = costmap[::-1]
scale = 3
resolution = resolution*3
costmap = costmap[::scale,::scale]
height, width = costmap.shape
for h in range(0,height):
    for w in range(0,width):
        if costmap[h,w]>205:
            grid.append([w*resolution, h*resolution])


grid = np.array(grid)
fg_map = fingerprint(X,y, grid)
heatmap = np.zeros([height,width])
for fg in fg_map:
    h = int(round(fg[1]/resolution))
    w = int(round(fg[0]/resolution))
    heatmap[h,w] = fg[2]

np.savetxt("heatmap/9s_sojourn.csv",
           heatmap, fmt='%f',
           delimiter=',', newline='\r\n')
plt.imshow(heatmap)
plt.show()



