#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import time
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

normal = np.loadtxt("resurvey_in_fingerprint/5G/normal.csv", dtype=float, delimiter=',')
outlier = np.loadtxt("resurvey_in_fingerprint/5G/outlier.csv", dtype=float, delimiter=',')
raw_fg = np.loadtxt("resurvey_in_fingerprint/5G/raw_fingerprint.csv", dtype=float, delimiter=',')

surveyed = np.loadtxt("resurvey_in_fingerprint/5G/surveyed.csv", dtype=float, delimiter=',')
resurveyed = np.loadtxt("resurvey_in_fingerprint/5G/resurveyed.csv", dtype=float, delimiter=',')
resurveyed_fg = np.loadtxt("resurvey_in_fingerprint/5G/resurveyed_fingerprint.csv", dtype=float, delimiter=',')

true_fg = np.loadtxt("resurvey_in_fingerprint/5G/ideal_fg.csv", dtype=float, delimiter=',')
# true_fg = np.loadtxt("resurvey_in_fingerprint/5G/ideal_fg_2.csv", dtype=float, delimiter=',')
# true_fg[true_fg[:,1]<]
# true_fg = np.loadtxt("6b/GP/0.5/meanRe.csv", dtype=float, delimiter=',')
# true_fg = np.column_stack((true_fg[:,:2],true_fg[:,1+7]))
# adjust

normal = normal[normal[:,1]>10]
normal = normal[np.argsort(normal[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/normal.csv",
           normal, fmt='%f',
           delimiter=',', newline='\r\n')
outlier = outlier[outlier[:,1]>10]
outlier = outlier[np.argsort(outlier[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/outlier.csv",
           outlier, fmt='%f',
           delimiter=',', newline='\r\n')
raw_fg =raw_fg[raw_fg[:,1]>10]
raw_fg =raw_fg[raw_fg[:,0]<49.4]
raw_fg = raw_fg[np.argsort(raw_fg[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/raw_fingerprint.csv",
           raw_fg, fmt='%f',
           delimiter=',', newline='\r\n')
surveyed = surveyed[surveyed[:,1]>10]
surveyed = surveyed[np.argsort(surveyed[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/surveyed.csv",
           surveyed, fmt='%f',
           delimiter=',', newline='\r\n')
resurveyed = resurveyed[resurveyed[:,1]>10]
resurveyed = resurveyed[np.argsort(resurveyed[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/resurveyed.csv",
           resurveyed, fmt='%f',
           delimiter=',', newline='\r\n')
resurveyed_fg = resurveyed_fg[resurveyed_fg[:,1]>10]
resurveyed_fg =resurveyed_fg[resurveyed_fg[:,0]<49.4]
resurveyed_fg = resurveyed_fg[np.argsort(resurveyed_fg[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/resurveyed_fingerprint.csv",
           resurveyed_fg, fmt='%f',
           delimiter=',', newline='\r\n')
true_fg = true_fg[true_fg[:,1]>10]
true_fg =true_fg[true_fg[:,0]<49.4]
true_fg = true_fg[np.argsort(true_fg[:, 1])]
np.savetxt("resurvey_in_fingerprint/5G/ideal_fg.csv",
           true_fg, fmt='%f',
           delimiter=',', newline='\r\n')
# ax = plt.figure().add_subplot(111, projection='3d')
# ax.scatter(normal[:,0], normal[:,1], normal[:,2], c='r', label = "normal")
#
# ax.scatter(outlier[:,0], outlier[:,1], outlier[:,2], c='black', label = "outlier")
#
# ax.scatter(raw_fg[:,0], raw_fg[:,1], raw_fg[:,2], c='g', label = "raw_fg")
#
# ax = plt.figure().add_subplot(111, projection='3d')
# ax.scatter(surveyed[:,0], surveyed[:,1], surveyed[:,2], c='r', label = "surveyed")
#
# ax.scatter(resurveyed[:,0], resurveyed[:,1], resurveyed[:,2], c='b', label = "resurveyed")
#
# ax.scatter(resurveyed_fg[:,0], resurveyed_fg[:,1], resurveyed_fg[:,2], c='g', label = "resurveyed_fg")
plt.rcParams["font.size"] = 14
plt.figure()
plt.scatter(normal[:,1], normal[:,2], c='r', label = 'Normal Signal')
plt.scatter(outlier[:,1], outlier[:,2], c='black', label = 'Abnormal Signal')
plt.plot(raw_fg[:,1], raw_fg[:,2], c='darkorange', lw = 2, label = 'Actual Fingerprint Map')
plt.plot(true_fg[:,1], true_fg[:,2], c='turquoise', lw = 2, label = 'Ideal Fingerprint Map')
plt.ylim([-80, -20])
plt.legend()
plt.xlabel("X (m)")
plt.ylabel('RSSI (dBm)')
plt.tight_layout()

plt.figure()
plt.scatter(surveyed[:,1], surveyed[:,2], c='r', label = 'Signal in Survey')
plt.scatter(resurveyed[:,1], resurveyed[:,2], c='b', label = 'Signal in Resurvey')
plt.plot(resurveyed_fg[:,1], resurveyed_fg[:,2], c='darkorange', lw = 2, label = 'Actual Fingerprint Map')
plt.plot(true_fg[:,1], true_fg[:,2], c='turquoise', lw = 2, label = 'Ideal Fingerprint Map')
plt.ylim([-80, -20])
plt.legend()
plt.xlabel("X (m)")
plt.ylabel('RSSI (dBm)')
plt.tight_layout()
plt.show()