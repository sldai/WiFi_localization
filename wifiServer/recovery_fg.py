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

measured = np.loadtxt("recover_in_fingerprint/5G/measured.csv", dtype=float, delimiter=',')
lost = np.loadtxt("recover_in_fingerprint/5G/lost.csv", dtype=float, delimiter=',')
raw_fg = np.loadtxt("recover_in_fingerprint/5G/raw_fingerprint.csv", dtype=float, delimiter=',')

recovered = np.loadtxt("recover_in_fingerprint/5G/recovered.csv", dtype=float, delimiter=',')
resurveyed_fg = np.loadtxt("recover_in_fingerprint/5G/recover_fingerprint.csv", dtype=float, delimiter=',')

true_fg = np.loadtxt("recover_in_fingerprint/5G/ideal_fg.csv", dtype=float, delimiter=',')
# true_fg = np.loadtxt("resurvey_in_fingerprint/2G/ideal_fg_2.csv", dtype=float, delimiter=',')
# true_fg[true_fg[:,1]<]
# true_fg = np.loadtxt("6b/GP/0.5/meanRe.csv", dtype=float, delimiter=',')
# true_fg = np.column_stack((true_fg[:,:2],true_fg[:,1+7]))
# adjust

measured = measured[measured[:,1]>10]
measured = measured[np.argsort(measured[:, 1])]
np.savetxt("recover_in_fingerprint/5G/measured.csv",
           measured, fmt='%f',
           delimiter=',', newline='\r\n')
lost = lost[lost[:,1]>10]
lost = lost[np.argsort(lost[:, 1])]
np.savetxt("recover_in_fingerprint/5G/lost.csv",
           lost, fmt='%f',
           delimiter=',', newline='\r\n')
raw_fg =raw_fg[raw_fg[:,1]>10]
raw_fg =raw_fg[raw_fg[:,0]<49.4]
raw_fg = raw_fg[np.argsort(raw_fg[:, 1])]
np.savetxt("recover_in_fingerprint/5G/raw_fingerprint.csv",
           raw_fg, fmt='%f',
           delimiter=',', newline='\r\n')


recovered = recovered[recovered[:,1]>10]
recovered = recovered[np.argsort(recovered[:, 1])]
np.savetxt("recover_in_fingerprint/5G/recovered.csv",
           recovered, fmt='%f',
           delimiter=',', newline='\r\n')
resurveyed_fg = resurveyed_fg[resurveyed_fg[:,1]>10]
resurveyed_fg =resurveyed_fg[resurveyed_fg[:,0]<49.4]
resurveyed_fg = resurveyed_fg[np.argsort(resurveyed_fg[:, 1])]
np.savetxt("recover_in_fingerprint/5G/recover_fingerprint.csv",
           resurveyed_fg, fmt='%f',
           delimiter=',', newline='\r\n')
true_fg = true_fg[true_fg[:,1]>10]
true_fg =true_fg[true_fg[:,0]<49.4]
true_fg = true_fg[np.argsort(true_fg[:, 1])]
np.savetxt("recover_in_fingerprint/5G/ideal_fg.csv",
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
plt.scatter(measured[:,1], measured[:,2], c='r', label = 'Normal Signal')
plt.scatter(lost[:,1], lost[:,2], c='black', label = 'Abnormal Signal')
plt.plot(raw_fg[:,1], raw_fg[:,2], c='darkorange', lw = 2, label = 'Actual Fingerprint Map')
plt.plot(true_fg[:,1], true_fg[:,2], c='turquoise', lw = 2, label = 'Ideal Fingerprint Map')
plt.ylim([-80, -20])
plt.legend()
plt.xlabel("X (m)")
plt.ylabel('RSSI (dBm)')
plt.tight_layout()

plt.figure()
plt.scatter(measured[:,1], measured[:,2], c='r', label = 'Normal Signal')

plt.scatter(recovered[:,1], recovered[:,2], c='b', label = 'Signal in Resurvey')
plt.plot(resurveyed_fg[:,1], resurveyed_fg[:,2], c='darkorange', lw = 2, label = 'Actual Fingerprint Map')
plt.plot(true_fg[:,1], true_fg[:,2], c='turquoise', lw = 2, label = 'Ideal Fingerprint Map')
plt.ylim([-80, -20])
plt.legend()
plt.xlabel("X (m)")
plt.ylabel('RSSI (dBm)')
plt.tight_layout()
plt.show()