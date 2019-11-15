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
from sklearn.preprocessing import StandardScaler
import copy
class DetectOutlier:
    def __init__(self, raw_fingerprints, map_setting, thereshold, resurvey_point):
        self.raw_fingerprints = raw_fingerprints.copy()
        self.ap_num = map_setting['ap_num']
        self.origin = map_setting['origin']
        self.interval = map_setting['interval']
        self.residues = []
        self.kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
                     + WhiteKernel(noise_level=20)
        self.GP = GaussianProcessRegressor(kernel=self.kernel, normalize_y=True)
        self.threshold = thereshold
        self.outlier_fingerprints = []
        self.resurvey_point = copy.deepcopy(resurvey_point)
        self.scaler = None

        self.coord_num = 2
        self.time_num = 1
        self.not_signal = self.coord_num+self.time_num


    def process(self):
        X = self.raw_fingerprints[:, self.time_num:self.coord_num+self.time_num]
        self.scaler = StandardScaler().fit(X)

        for ap_index in range(self.ap_num*2):
            effective_index = self.raw_fingerprints[:,self.not_signal+ap_index] != -100
            time_index = self.raw_fingerprints[effective_index,:self.time_num]
            X = self.raw_fingerprints[effective_index,self.time_num:self.not_signal]
            y = self.raw_fingerprints[effective_index,self.not_signal+ap_index]
            while True:
                if len(X) < 10:
                    break
                self.GP.fit(self.scaler.transform(X), y)
                index = self.calc_residue(X, y)
                if index == -1:
                    break
                else:
                    outlier = np.zeros([self.ap_num*2+self.not_signal])
                    outlier[:self.time_num] = time_index[index]
                    outlier[self.time_num:self.not_signal] = X[index,:self.coord_num]
                    outlier[self.not_signal+ap_index] = y[index]
                    self.outlier_fingerprints.append(outlier)

                    time_index = np.delete(time_index, index, axis=0)
                    X = np.delete(X, index, axis=0)
                    y = np.delete(y, index, axis=0)
            self.update_target(self.outlier_fingerprints)

        self.outlier_fingerprints = np.array(self.outlier_fingerprints)


    def calc_residue(self, X, y):
        y_gpr, y_std = self.GP.predict(self.scaler.transform(X), return_std=True)
        residue = (y - y_gpr)

        residue = ([abs(residue[i] / std) for i, std in enumerate(y_std)])
        index = None
        if max(residue) < self.threshold:
            index = -1
        else:
            index = residue.index(max(residue))
        return index

    def update_target(self, outliers):
        for outlier in outliers:
            tmp_x = round((outlier[self.time_num+0]-self.origin[0])/self.interval)*self.interval + self.origin[0]
            tmp_y = round((outlier[self.time_num+1]-self.origin[1])/self.interval)*self.interval + self.origin[1]
            outlier_point = [tmp_x, tmp_y]
            if outlier_point not in self.resurvey_point:
                self.resurvey_point.append(outlier_point)

    def GetRawFingerprints(self):
        return self.raw_fingerprints.copy()

    def GetOutlierFingerprints(self):
        return self.outlier_fingerprints.copy()

    def get_target_list(self):
        return copy.deepcopy(self.resurvey_point)





if __name__ == '__main__':
    map_setting = {'ap_num': 5, 'interval': 0.8, 'origin': [0.0,0.0]}
    dataRaw = np.loadtxt("E:/WiFi/day1/3F/0.5 m per s.csv", dtype=float, delimiter=',')[:, 1:]
    process2 = DetectOutlier(dataRaw, map_setting, 2, [])
    process2.process()
    raw_fingerprints = process2.GetRawFingerprints()
    outliers = process2.GetOutlierFingerprints()

    # plot
    for i in range(map_setting['ap_num']*2):
        X = raw_fingerprints[:,:2]
        y = raw_fingerprints[:,2+i]
        oX = outliers[:,:2]
        oy = outliers[:,2+i]
        ax = plt.figure().add_subplot(111, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], y[:], c='r', label='mearsured')
        ax.scatter(oX[:, 0], oX[:, 1], oy[:], c='g', label='outlier')

    plt.show()
    # plot outliers
    #
    # ax.set_title(str(ap))
    #
    # ax.scatter(X[index_measured, 0], X[index_measured, 1], y_gpr[index_measured], c='g', label = 'estimated')
    # if len(outliers) > 0:
    #     outliers = np.array(outliers)
    #     ax.scatter(outliers[index_outlier, 0], outliers[index_outlier, 1], outliers[index_outlier, 2], c='b', label = 'outlier')
    # ax.legend()
