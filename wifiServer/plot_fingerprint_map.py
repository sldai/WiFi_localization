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
# use 6f 0.3m csv
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/0.9m.csv", dtype=float, delimiter=',')[:,1:]
ap_num = 10
ap2_index = 1+10+ap_num
ap5_index = ap2_index-ap_num
map_setting = {'ap_num': ap_num, 'interval': 0.8, 'origin': [0.0, 0.0], 'lost_signal': -100}
grid_6F = np.loadtxt("candidate6.csv", dtype=float, delimiter=',')[:]
grid_6F = np.arange(12.7,73.7,0.1)
grid_6F_tmp = np.zeros([len(grid_6F), 2])
grid_6F_tmp[:,1] = grid_6F
grid_6F_tmp[:,0] = 49.364
grid_6F = grid_6F_tmp
# grid_6F = grid_6F[grid_6F[:,0]<49.5]
def fingerprint(X, y, grid):
    kernel = 2.0 * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1.0)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    scaler = StandardScaler().fit(X)
    gpr.fit(scaler.transform(X), y)
    y_gpr, y_std = gpr.predict(scaler.transform(grid), return_std=True)

    return np.column_stack((grid, y_gpr, y_std))
fg = np.row_stack(np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static - 副本.csv", dtype=float, delimiter=','))
# fg_add = np.loadtxt("resurvey_in_fingerprint/5G/resurveyed.csv", dtype=float, delimiter=',')
# fg_add = np.row_stack((fg_add[29:35],fg_add[176:184]))
fg = np.column_stack((fg[:,:2],fg[:,ap2_index]))
# for i in range(2):
#     fg = np.row_stack((fg,fg_add))
fg = fg[fg[:,2]!=-100]
ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(fg[:, 0], fg[:, 1], fg[:,2], c='black')
fg = fingerprint(fg[:,:2],fg[:,2],grid_6F)


ax.scatter(fg[:, 0], fg[:, 1], fg[:,2], c='g')

np.savetxt("recover_in_fingerprint/5G/ideal_fg.csv",
           fg, fmt='%f',
           delimiter=',', newline='\r\n')
# plt.show()
########### plot unrecovered ########
measured_index = data[:,ap2_index]!= -100
lost_index = data[:,ap2_index] == -100
recovered_index = (data[:,ap2_index] == -100) & (data[:,ap5_index] != -100)
recover_pro = Recover(map_setting=map_setting, raw_fingerprints=data)
recover_pro.recover_process()
recovered = recover_pro.GetResult()
# plot lost

ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(data[lost_index, 0], data[lost_index, 1], data[lost_index, ap2_index], c='black', label = "lost")
np.savetxt("recover_in_fingerprint/5G/lost.csv", np.column_stack((data[lost_index, :2], data[lost_index, ap2_index])), fmt='%f', delimiter=',',newline='\r\n')
# plot measured
ax.scatter(data[measured_index, 0], data[measured_index, 1], data[measured_index, ap2_index], c='r', label = "measured")

# plot fingerprint
fg = fingerprint(data[:,:2], data[:, ap2_index], grid_6F)
ax.scatter(fg[:, 0], fg[:, 1], fg[:, 2], c='g', label = "fingerprint map")
np.savetxt("recover_in_fingerprint/5G/raw_fingerprint.csv", fg, fmt='%f', delimiter=',',newline='\r\n')
########## plot recovered #######
ax = plt.figure().add_subplot(111, projection='3d')

# plot lost
ax.scatter(recovered[lost_index & (~recovered_index), 0], recovered[lost_index & (~recovered_index), 1], recovered[lost_index & (~recovered_index), ap2_index], c='black', label = "lost")
tmp = recovered[lost_index & (~recovered_index), :]

# plot measured
ax.scatter(recovered[measured_index, 0], recovered[measured_index, 1], recovered[measured_index, ap2_index], c='r', label = "measured")
np.savetxt("recover_in_fingerprint/5G/measured.csv", np.column_stack((recovered[measured_index, :2], recovered[measured_index, ap2_index])), fmt='%f', delimiter=',',newline='\r\n')
# plot recovered
ax.scatter(recovered[recovered_index, 0], recovered[recovered_index, 1], recovered[recovered_index, ap2_index], c='b', label = "recovered")
np.savetxt("recover_in_fingerprint/5G/recovered.csv", np.column_stack((recovered[recovered_index, :2], recovered[recovered_index, ap2_index])), fmt='%f', delimiter=',',newline='\r\n')
# plot fingerprint
fg = fingerprint(recovered[:,:2], recovered[:, ap2_index], grid_6F)
ax.scatter(fg[:, 0], fg[:, 1], fg[:, 2], c='g', label = "fingerprint map")
np.savetxt("recover_in_fingerprint/5G/recover_fingerprint.csv", fg, fmt='%f', delimiter=',',newline='\r\n')
import time
########## plot surveyed ##########
survey_data = recovered
process2 = DetectOutlier(survey_data, map_setting, 1.8, [])
# current_time = time.time()
process2.process_one_ap_for_show(ap2_index-1)
# print('time :'+str(time.time()-current_time))
raw_fingerprints = process2.GetRawFingerprints()
outliers = process2.GetOutlierFingerprints()

for outlier in outliers:
    if outlier[ap2_index]!=0:
        for raw_fg in raw_fingerprints:
            if raw_fg[0] == outlier[0] and raw_fg[1] == outlier[1] and raw_fg[ap2_index] == outlier[ap2_index]:
                raw_fg[ap2_index] = 0
outlier_index = outliers[:, ap2_index] != 0

normal_index = raw_fingerprints[:,ap2_index] != 0
raw_fingerprints = process2.GetRawFingerprints()
# plot normal one
ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(raw_fingerprints[normal_index, 0], raw_fingerprints[normal_index, 1], raw_fingerprints[normal_index, ap2_index], c='r', label = "normal")
for_plot = np.column_stack((raw_fingerprints[normal_index, 0], raw_fingerprints[normal_index, 1], raw_fingerprints[normal_index, ap2_index]))
# np.savetxt("resurvey_in_fingerprint/5G/normal.csv", for_plot, fmt='%f', delimiter=',', newline='\r\n')
# plot outliers
ax.scatter(outliers[outlier_index, 0], outliers[outlier_index, 1], outliers[outlier_index, ap2_index], c='b', label = "outlier")
for_plot = np.column_stack((outliers[outlier_index, 0], outliers[outlier_index, 1], outliers[outlier_index, ap2_index]))
# np.savetxt("resurvey_in_fingerprint/5G/outlier.csv", for_plot, fmt='%f', delimiter=',', newline='\r\n')
# plot fingerprint
fg = fingerprint(raw_fingerprints[normal_index,:2], raw_fingerprints[normal_index, ap2_index], grid_6F)
ax.scatter(fg[:, 0], fg[:, 1], fg[:, 2], c='g', label = "fingerprint map")
# np.savetxt("resurvey_in_fingerprint/5G/raw_fingerprint.csv", fg, fmt='%f', delimiter=',', newline='\r\n')

########## plot resurveyed ######
data_sojourn = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static.csv", dtype=float, delimiter=',')
def get_resurveyed_data(resurvey_list):
    extra_fingerprint_list = []
    for point in resurvey_list:
        for fingerprint in data_sojourn:
            if np.linalg.norm(fingerprint[:2] - point) < 0.8/2:
                extra_fingerprint_list.append(fingerprint)
    return np.array(extra_fingerprint_list)
oo = process2.get_resurvey_point()
oo.append([49.3, 58])
data_resurveyed = get_resurveyed_data(oo)
combine_raw_resurveyed = np.row_stack((data, data_resurveyed))
recover_pro = Recover(map_setting=map_setting, raw_fingerprints=combine_raw_resurveyed)
recover_pro.recover_process()
recovered = recover_pro.GetResult()
# plot surveyed
ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(recovered[:len(data), 0], recovered[:len(data), 1], recovered[:len(data), ap2_index], c='r', label = "surveyed")
for_plot = np.column_stack((recovered[:len(data), 0], recovered[:len(data), 1], recovered[:len(data), ap2_index]))
# np.savetxt("resurvey_in_fingerprint/5G/surveyed.csv", for_plot, fmt='%f', delimiter=',', newline='\r\n')
# plot resurveyed
ax.scatter(recovered[len(data):, 0], recovered[len(data):, 1], recovered[len(data):, ap2_index], c='b', label = "normal")
for_plot = np.column_stack((recovered[len(data):, 0], recovered[len(data):, 1], recovered[len(data):, ap2_index]))
# np.savetxt("resurvey_in_fingerprint/5G/resurveyed.csv", for_plot, fmt='%f', delimiter=',', newline='\r\n')
# plot fingerprint

fg = fingerprint(recovered[:,:2], recovered[:, ap2_index], grid_6F)
ax.scatter(fg[:, 0], fg[:, 1], fg[:, 2], c='g', label = "fingerprint map")
# np.savetxt("resurvey_in_fingerprint/5G/resurveyed_fingerprint.csv", fg, fmt='%f', delimiter=',', newline='\r\n')
plt.show()