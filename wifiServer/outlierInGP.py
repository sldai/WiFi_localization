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
from outliers import smirnov_grubbs as grubbs
from scipy import stats
from sklearn.preprocessing import StandardScaler
from copy import deepcopy
class DetectOutlier:
    def __init__(self, raw_fingerprints, map_setting, thereshold, resurvey_point):
        self.raw_fingerprints = raw_fingerprints.copy()
        self.ap_num = map_setting['ap_num']
        self.origin = map_setting['origin']
        self.interval = map_setting['interval']
        self.residues = []
        self.kernel = 2.0 * RBF(length_scale=5.0, length_scale_bounds=(1e-2, 1e3)) \
                     + WhiteKernel(noise_level=5)
        self.GP = GaussianProcessRegressor(kernel=self.kernel, normalize_y=True)
        self.threshold = thereshold
        self.outlier_fingerprints = []
        self.resurvey_point = resurvey_point
        self.scaler = None


    def process_one_ap_for_show(self, show_ap_index):
        # just for figure in paper
        X = self.raw_fingerprints[:, :2]
        self.scaler = StandardScaler().fit(X)

        for ap_index in range(show_ap_index-1,show_ap_index):
            effective_index = self.raw_fingerprints[:,2+ap_index] != -100
            X = self.raw_fingerprints[effective_index,:2]
            y = self.raw_fingerprints[effective_index,2+ap_index]
            if len(X)<10:
                break
            while True:
                self.GP.fit(self.scaler.transform(X), y)
                index = self.calc_residue(X, y)
                if index == -1:
                    break
                else:
                    outlier = np.zeros([self.ap_num*2+2])
                    outlier[:2] = X[index,:2]
                    outlier[2+ap_index] = y[index]
                    self.outlier_fingerprints.append(outlier)

                    X = np.delete(X, index, axis=0)
                    y = np.delete(y, index, axis=0)
            self.update_target(self.outlier_fingerprints)

        self.outlier_fingerprints = np.array(self.outlier_fingerprints)

    def process(self):
        X = self.raw_fingerprints[:, :2]
        self.scaler = StandardScaler().fit(X)

        for ap_index in range(2*self.ap_num):
            effective_index = self.raw_fingerprints[:,2+ap_index] != -100
            X = self.raw_fingerprints[effective_index,:2]
            y = self.raw_fingerprints[effective_index,2+ap_index]
            if len(X)<10:
                break
            while True:
                self.GP.fit(self.scaler.transform(X), y)
                index = self.calc_residue(X, y)
                if index == -1:
                    break
                else:
                    outlier = np.zeros([self.ap_num*2+2])
                    outlier[:2] = X[index,:2]
                    outlier[2+ap_index] = y[index]
                    self.outlier_fingerprints.append(outlier)

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
            tmp_x = round((outlier[0]-self.origin[0])/self.interval)*self.interval + self.origin[0]
            tmp_y = round((outlier[1]-self.origin[1])/self.interval)*self.interval + self.origin[1]
            outlier_point = [tmp_x, tmp_y]
            if outlier_point not in self.resurvey_point:
                self.resurvey_point.append(outlier_point)

    def GetRawFingerprints(self):
        return self.raw_fingerprints.copy()

    def GetOutlierFingerprints(self):
        return self.outlier_fingerprints.copy()

    def get_resurvey_point(self):
        return deepcopy(self.resurvey_point)


def detect_outliers(training_raw):
    ap_num = 19
    scaler = StandardScaler().fit(training_raw[:,1:1+2])
    for ap in range(1):
        training_data = training_raw[training_raw[:, ap+2] != -100, :]
        if len(training_data) <= 100:
            continue
        kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
                 + WhiteKernel(noise_level=1)
        gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
        X = training_data[:, :2]
        y = training_data[:, ap+2]

        outliers = []
        y_gpr, y_std = None, None
        while True:
            gpr.fit(scaler.transform(X), y)
            y_gpr, y_std = gpr.predict(scaler.transform(X), return_std=True)
            residue = (y - y_gpr)

            residue = ([abs(residue[i]/std) for i, std in enumerate(y_std)])
            if max(residue) < 2:
                break
            index = residue.index(max(residue))

            # index = grubbs.test_once(residue)
            if index is None:
                break

            outlier = np.array([X[index, 0], X[index, 1], y[index]])
            outliers.append(outlier)

            X = np.delete(X, index, axis=0)
            y = np.delete(y, index, axis=0)
            training_data = np.delete(training_data, index, axis=0)

        outliers = np.array(outliers)

        X[:, 1] = np.round(X[:, 1])

        index_measured = X[:, 1] == 76
        outliers[:, 1] = np.round(outliers[:, 1])
        index_outlier = outliers[:, 1] == 76
        # ax = plt.figure().add_subplot(111, projection='3d')
        # ax.set_title(str(ap))
        # ax.scatter(X[index_measured, 0], X[index_measured, 1], y[index_measured], c='r', label = 'mearsured')
        # ax.scatter(X[index_measured, 0], X[index_measured, 1], y_gpr[index_measured], c='g', label = 'estimated')
        # if len(outliers) > 0:
        #     outliers = np.array(outliers)
        #     ax.scatter(outliers[index_outlier, 0], outliers[index_outlier, 1], outliers[index_outlier, 2], c='b', label = 'outlier')
        # ax.legend()

        figure = plt.figure()
        measured_sort = np.argsort(X[index_measured, 0])
        plt.scatter((X[index_measured, 0])[measured_sort], (y[index_measured])[measured_sort], c='b', label = 'normal')
        plt.plot((X[index_measured, 0])[measured_sort], (y_gpr[index_measured])[measured_sort], c='darkorange', label = 'fitting')
        plt.fill_between((X[index_measured, 0])[measured_sort], (y_gpr[index_measured] - y_std[index_measured])[measured_sort], (y_gpr[index_measured] + y_std[index_measured])[measured_sort], color='darkorange',
                         alpha=0.2)
        if len(outliers) > 0:
            plt.scatter(outliers[index_outlier, 0], outliers[index_outlier, 2], c='r', label='outlier')
        plt.legend()
        plt.xlabel('X (m)')
        plt.ylabel('RSSI (dBm)')
        plt.tight_layout()

if __name__ == '__main__':
    map_setting = {'ap_num': 19, 'interval': 0.8, 'origin': [0.0,0.0]}
    dataRaw = np.loadtxt("survey_results/resurveyed/survey0.csv", dtype=float, delimiter=',')[:, 1:]
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
