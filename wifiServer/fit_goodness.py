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
from sklearn.model_selection import KFold

def even_split_train_test(X, y, n):
    fold_X = []
    fold_y = []
    for i in range(n):
        fold_X.append(X[i::n])
        fold_y.append(y[i::n])

    even_KFold = []
    for i in range(n):
        test_data_X = fold_X[i]
        test_data_y = fold_y[i]

        training_data_X = []
        training_data_y = []
        for j in range(n):
            if j == i:
                continue
            training_data_X.extend(fold_X[j].tolist())
            training_data_y.extend(fold_y[j].tolist())
        training_data_X = np.array(training_data_X)
        training_data_y = np.array(training_data_y)
        even_KFold.append((training_data_X, training_data_y, test_data_X, test_data_y))
    return even_KFold.copy()


def fit_goodness_Gaussian(X, y, n):
    kernel = 2.0 * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1.0)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    scaler = StandardScaler().fit(X)

    even_KFold = even_split_train_test(X, y, n)
    error = []
    for training_data_X, training_data_y, test_data_X, test_data_y in even_KFold:
        gpr.fit(scaler.transform(training_data_X), training_data_y)
        y_gpr, y_std = gpr.predict(scaler.transform(test_data_X), return_std=True)
        tmp_err = (y_gpr-test_data_y).tolist()
        error.extend(tmp_err)
    return np.array(error)

def fit_goodness_svr(X, y, n):
    kernel = 2.0 * RBF(length_scale=10.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1.0)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    scaler = StandardScaler().fit(X)

    even_KFold = even_split_train_test(X, y, n)
    error = []
    for training_data_X, training_data_y, test_data_X, test_data_y in even_KFold:
        gpr.fit(scaler.transform(training_data_X), training_data_y)
        y_gpr, y_std = gpr.predict(scaler.transform(test_data_X), return_std=True)
        tmp_err = (y_gpr-test_data_y).tolist()
        error.extend(tmp_err)
    return np.array(error)

if __name__ == '__main__':
    # read data of the floor
    data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/0.3m.csv", dtype=float, delimiter=',')
    X = data[:,:2]
    y = data[:, 16]
    n = 5
    whole_error = fit_goodness_Gaussian(X, y, n)
    np.savetxt("fit_goodness/whole_error.csv",
               whole_error, fmt='%f',
               delimiter=',', newline='\r\n')

    # read data of regions
    region1 = 495
    error1 = fit_goodness_Gaussian(X[:region1], y[:region1], n)
    error2 = fit_goodness_Gaussian(X[region1:], y[region1:], n)
    np.savetxt("fit_goodness/region_error.csv",
               np.array(error1.tolist()+error2.tolist()), fmt='%f',
               delimiter=',', newline='\r\n')