#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.semi_supervised import label_propagation
from sklearn.datasets import make_circles
from sklearn import svm
import math
from mpl_toolkits.mplot3d import Axes3D
import scipy.io as scio
completeGrid = scio.loadmat('6b' + "/grid/complete/" + 'grid.mat')
completeGrid = completeGrid['grid']
grid = scio.loadmat('6b' + "/grid/0.3m/" + 'diff.mat')
origin = scio.loadmat('6b' + "/grid/0.3m/" + 'origin.mat')
grid = grid['grid']
origin = origin['origin'][0]
data=np.loadtxt("E:/project/PycharmProjects/wifiServer/csv/restore data.csv", dtype=float, delimiter=',')
def labeling(array):
    cluster = 10
    sortarray = array[array[:] != -100]
    totalNum = len(array)

    for i in range(totalNum):
        if array[i] == -1:
            array[i] = -1
            continue
        #array[i] = int(round((array[i]+95)/10))
        array[i] = (round((array[i] + 95)/1 ))

    return array
row = grid.shape[0]
col = grid.shape[1]
trainingData = []

for i in range(row):
    for j in range(col):
        if completeGrid[i, j,0] != 0:
            if grid[i, j,0] != 0:
                temp = np.linspace(0,0,22)
                temp[0]=j+origin[0]
                temp[1]=i+origin[1]
                temp[2:]=grid[i,j,:]
                trainingData.append(temp)
            elif grid[i, j,0] == 0:
                temp = np.linspace(0, 0, 22)
                temp[0] = j + origin[0]
                temp[1] = i + origin[1]
                temp[2:] = -1
                trainingData.append(temp)
trainingData = np.array(trainingData)
dataTrain = data
dataPre = trainingData[trainingData[:,2]==-1,:]
trainingData = np.r_[dataTrain,dataPre]
ax = []
for Ap in range(20):
    ApIndex = Ap+2
    y = labeling(trainingData[:,ApIndex])

    X = trainingData[:,:2]
    # Learn with LabelSpreading

    label_spread = label_propagation.LabelSpreading(kernel='rbf', gamma=0.1, alpha=0.15)
    label_spread.fit(X, y)

    output_labels = label_spread.transduction_
    trainingData[:,ApIndex] = output_labels-95
    ax.append(plt.figure().add_subplot(111, projection='3d'))
    ax[Ap].scatter(X[:len(dataTrain),0], X[:len(dataTrain),1], y[:len(dataTrain)], c='r')

    ax[Ap].scatter(X[len(dataTrain):,0], X[len(dataTrain):,1], y[len(dataTrain):], c='g')
np.savetxt("csv/completeGrid.csv",np.r_[data,trainingData[len(dataTrain):,:]],fmt='%f',delimiter=',',newline='\r\n')
plt.show()