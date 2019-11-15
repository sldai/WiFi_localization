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
from restore import Restore
from sklearn.preprocessing import StandardScaler
rng = np.random.RandomState(0)
# data1 = np.loadtxt("E:/WiFi/day1/3F/0 m per s.csv", dtype=float, delimiter=',')[:,1:]
#
# data3 = np.loadtxt("E:/WiFi/day3/1.5 m per s.txt", dtype=float, delimiter=',')[:,1:]
#
# data4 = np.loadtxt("E:/WiFi/day4/1.5 m per s.txt", dtype=float, delimiter=',')[:,1:]
#
# data5 = np.loadtxt("E:/WiFi/day5/1.5 m per s.txt", dtype=float, delimiter=',')[:,1:]
data1 = np.loadtxt("E:/WiFi/day2/1.5 m per  s.txt", dtype=float, delimiter=',')[:,1:]
data2 = np.loadtxt("E:/project/PycharmProjects/wifiServer/3F/GP/0/meanRe.csv", dtype=float, delimiter=',')
dataAll = np.r_[data1, data2]
TrainChoice = range(0, len(dataAll), 1)
dataAll=dataAll[TrainChoice]
grid = np.loadtxt("candidate.csv", dtype=float, delimiter=',')
#grid = np.array(dataAll[:,:2])
gridMean = np.array(grid)
gridStd = np.array(grid)
default = -90
# dataAll[dataAll[:,:]==-100] = default

# testdataAll  = np.loadtxt("E:/WiFi/实验室6楼/wifiData/行人验证/lastpdr.csv", dtype=float, delimiter=',')
# testdataAll = testdataAll[testdataAll[:,1]==2,2:]
testdataAll  = np.loadtxt("E:/WiFi/day1/3F/2 m per s.csv", dtype=float, delimiter=',')[:,1:]
# testdataAll  = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/1.2m_human.csv", dtype=float, delimiter=',')[:,3:]
font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,}
modelPath = 'model/GP/'
inputNum = 2
interval = 19
scaler = StandardScaler().fit(dataAll[:,:inputNum])
ax = []
err = np.zeros([len(testdataAll),len(testdataAll[0])-2])
for Ap in range(0,interval):
    testAP = inputNum + Ap
    testAPBand = testAP + interval
    testdata = testdataAll[testdataAll[:,testAP]!=-100,:]
    dataRaw = dataAll[dataAll[:, testAP] != -100]
    y,dy,reData = Restore(dataAll=dataAll,gap=interval,inputN=inputNum,num=Ap)
    y[y[:]==-100]=default

    X = dataAll[:,:inputNum]

    kernel = 1.0* RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
             +WhiteKernel(noise_level=1)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    stime = time.time()
    gpr.fit(scaler.transform(X), y)
    print("Time for GPR fitting: %.3f" % (time.time() - stime))

    X_predict =grid[:,:2]
    # Predict using gaussian process regressor

    stime = time.time()
    y_gpr, y_std = gpr.predict(scaler.transform(X_predict), return_std=True)
    gridMean = np.c_[gridMean,y_gpr]
    gridStd = np.c_[gridStd, y_std]
    print("Time for GPR prediction with standard-deviation: %.3f"
          % (time.time() - stime))
    print(gpr.kernel_)
    #print(y_gpr-testdata[:,testAPBand])

    # Plot results
    ax.append(plt.figure().add_subplot(111, projection='3d'))

    ax[Ap].scatter(dataRaw[:, 0], dataRaw[:, 1], dataRaw[:,testAP], c='r')
    dataUndetect = dataAll[dataAll[:, testAP] == -100]
    # ax[Ap].scatter(reData[:, 0], reData[:, 1], reData[:, testAP], c='black')

    ax[Ap].scatter(dataUndetect[:, 0], dataUndetect[:, 1], dataUndetect[:, testAP], c='b')

    ax[Ap].scatter(X_predict[:, 0], X_predict[:, 1], y_gpr[:], c='g')
    # if Ap ==9:
    #     np.savetxt("csv/measured.csv", np.array(np.c_[dataRaw[:, 0], dataRaw[:, 1], dataRaw[:,testAP]]), fmt='%f', delimiter=',', newline='\r\n')
    #     np.savetxt("csv/recovered.csv", np.array(np.c_[reData[:, 0], reData[:, 1], reData[:, testAP]]), fmt='%f',
    #                delimiter=',', newline='\r\n')
    #     np.savetxt("csv/undetected.csv", np.array(np.c_[dataUndetect[:, 0], dataUndetect[:, 1], dataUndetect[:, testAP]]), fmt='%f',
    #                delimiter=',', newline='\r\n')
    #     np.savetxt("csv/fingerprint.csv", np.array(np.c_[X_predict[:, 0], X_predict[:, 1], y_gpr[:]]), fmt='%f',
    #                delimiter=',', newline='\r\n')


    # ax[Ap].scatter(testdata[:, 0], testdata[:, 1], testdata[:,testAP], c='b')
    ax[Ap].set_zlabel('RSSI (dBm)',font1)  # 坐标轴
    ax[Ap].set_ylabel('Y (m)',font1)
    ax[Ap].set_xlabel('X (m)',font1)
    ax[Ap].legend(['measured data','undetected data','fingerprint map'],prop=font1,loc = 'lower center', bbox_to_anchor=(0.6,0.95))

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    joblib.dump(gpr, modelPath + "ap" + str(Ap) + ".pkl")
for Ap in range(interval,2*interval):
    testAP = inputNum + Ap

    # ignore the default RSSI
    data = dataAll[:, :]
    data = data[:]
    # trainingData, testingData = train_test_split(data, test_size=0.2)
    # trainingData=trainingData[trainingData[:,0].argsort()]
    # testingData = testingData[testingData[:, 0].argsort()]




    testdata = testdataAll[testdataAll[:, testAP] != -100, :]

    X = np.r_[data[:, 0:2]]
    # X_show = np.r_[trainingData[:, 0].reshape(-1,1),testingData[:1,0].reshape(-1,1)]
    # X_show = X_show[X_show[:, 0].argsort()]
    # y = data[:,testAP]
    dataRaw = dataAll[dataAll[:, testAP] != -100]
    y, dy, reData = Restore(dataAll=dataAll, gap=-interval, inputN=inputNum, num=Ap)
    y[y[:]==-100]=default
    # dy = np.zeros(data[:, testAP].shape) + 4
    kernel = 1.0* RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
             +WhiteKernel(noise_level=1)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    stime = time.time()
    gpr.fit(scaler.transform(X), y)
    print("Time for GPR fitting: %.3f" % (time.time() - stime))


    X_predict = grid[:, :2]
    # Predict using gaussian process regressor

    stime = time.time()
    y_gpr, y_std = gpr.predict(scaler.transform(X_predict), return_std=True)
    gridMean = np.c_[gridMean, y_gpr]
    gridStd = np.c_[gridStd, y_std]
    print("Time for GPR prediction with standard-deviation: %.3f"
          % (time.time() - stime))
    ax.append(plt.figure().add_subplot(111, projection='3d'))
    ax[Ap].scatter(dataRaw[:, 0], dataRaw[:, 1], dataRaw[:, testAP], c='r')
    dataUndetect = dataAll[dataAll[:, testAP] == -100]
    # ax[Ap].scatter(reData[:, 0], reData[:, 1], reData[:, testAP], c='black')

    ax[Ap].scatter(dataUndetect[:, 0], dataUndetect[:, 1], dataUndetect[:, testAP], c='b')

    ax[Ap].scatter(X_predict[:, 0], X_predict[:, 1], y_gpr[:], c='g')
    # ax[Ap].scatter(testdata[:, 0], testdata[:, 1], testdata[:,testAP], c='b')
    ax[Ap].set_zlabel('RSSI (dBm)', font1)  # 坐标轴
    ax[Ap].set_ylabel('Y (m)', font1)
    ax[Ap].set_xlabel('X (m)', font1)
    ax[Ap].legend(['measured data',  'undetected data', 'fingerprint map'], prop=font1,
                  loc='lower center',bbox_to_anchor=(0.6,0.95))
    if Ap ==2*interval-1:
        np.savetxt("csv/measured.csv", np.array(np.c_[dataRaw[:, 0], dataRaw[:, 1], dataRaw[:,testAP]]), fmt='%f', delimiter=',', newline='\r\n')
        np.savetxt("csv/recovered.csv", np.array(np.c_[reData[:, 0], reData[:, 1], reData[:, testAP]]), fmt='%f',
                   delimiter=',', newline='\r\n')
        np.savetxt("csv/undetected.csv", np.array(np.c_[dataUndetect[:, 0], dataUndetect[:, 1], dataUndetect[:, testAP]]), fmt='%f',
                   delimiter=',', newline='\r\n')
        np.savetxt("csv/fingerprint.csv", np.array(np.c_[X_predict[:, 0], X_predict[:, 1], y_gpr[:]]), fmt='%f',
                   delimiter=',', newline='\r\n')
    # err[:len(y_gpr),Ap]=y_gpr-grid[:,testAP]
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    print(gpr.kernel_)

np.savetxt("6b/GP/sample/3/means.csv", np.array(gridMean), fmt='%f', delimiter=',', newline='\r\n')
np.savetxt("6b/GP/sample/3/stds.csv", np.array(gridStd), fmt='%f', delimiter=',', newline='\r\n')
# plt.xticks(())
# plt.yticks(())
plt.show()


