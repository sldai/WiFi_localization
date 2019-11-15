#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
import random as rand
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import math as mt
from nn_predict import NN_predict
import scipy.io as scio
modelPath="./model/svm/"
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-04-11 20_20_28.txt", dtype=float, delimiter=',')
testData = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-05-13 22_05_01.csv", dtype=float, delimiter=',')
dataWithout100=[]
apLocation=scio.loadmat('./6b/grid/apLocation.mat')
apLocation=apLocation['apLocation']
for num in range(20):
    temp=[]
    for i in range(len(data)):
        if data[i,2+num]!=-100:
            dis=((data[i,0]-apLocation[num,0])**2+(data[i,1]-apLocation[num,1])**2)**0.5
            temp.append([dis, data[i,2 + num]])

    dataWithout100.append(temp)

testdataWithout100=[]
for num in range(20):
    temp=[]
    for i in range(len(testData)):
        if testData[i,2+num]!=-100:
            dis=((testData[i,0]-apLocation[num,0])**2+(testData[i,1]-apLocation[num,1])**2)**0.5
            temp.append([dis, testData[i,2 + num]])

    testdataWithout100.append(temp)
ax = []
err=[]
for num in range(20):
    tempArray=np.array(dataWithout100[num])
    tempModel = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=10, epsilon=0.1, shrinking=True,
                   cache_size=200, verbose=False, max_iter=-1)
    X=tempArray[:, :1]
    temptestArray=np.array(testdataWithout100[num])
    print(X.shape[1])
    y=tempArray[:, 1]
    tempModel.fit(X,y)
    #joblib.dump(tempModel, modelPath + "ap" + str(num) + ".pkl")
    result=tempModel.predict(temptestArray[:, :1])
    #ax.append(plt.figure().add_subplot(111, projection='3d'))
    plt.figure()
    #plt.plot(temptestArray[:, 0], temptestArray[:, 1], '*r')
    plt.plot(temptestArray[:, 0], result[:], '*g')
    err.extend(result[:]-temptestArray[:, 1])
plt.show()
np.savetxt("radioSvrErr.csv",np.array(err),fmt='%f',delimiter=',',newline='\r\n')
