#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import numpy as np
from numpy import argsort
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.cross_validation import train_test_split
import random as rand
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import math as mt
import scipy.io as scio
from sklearn.externals import joblib
from particleFilterClass import particleFilter


apNum=10

testingData = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/1.2m_human.csv", dtype=float, delimiter=',')[:,1:]
pF=particleFilter(apNum,'GP','./6b')

KnnErr=[]
gpr = np.loadtxt("E:/project/PycharmProjects/wifiServer/3F/GP/1/meanRe.csv", dtype=float, delimiter=',')
std = np.loadtxt("E:/project/PycharmProjects/wifiServer/3F/GP/1/stdRe.csv", dtype=float, delimiter=',')
def GP(ob,n):
    nnlist = []
    for i in range(len(gpr)):
            x = gpr[i,0]
            y = gpr[i,1]
            p = 1
            for num in range(2*apNum):
                if ob[num] != -100:
                    u = gpr[i,2+num]
                    sigma = std[i,2+num]
                    p *= mt.exp(-(u - ob[num]) ** 2 / (2 * (sigma) ** 2)) / sigma * 10
            pro = p
            nnlist.append([x, y, pro])
    nnlist = np.array(nnlist)
    mean = [0, 0]
    nnlist = nnlist[np.lexsort(-nnlist.T)]
    nnlist = nnlist[:n]
    nnlist[:, 2] = nnlist[:, 2] / sum(nnlist[:, 2])
    for i in range(n):
        mean += nnlist[i, :2] * nnlist[i, 2]
    return mean
k=1
inputNum = 4
ini=pF.knn(testingData[0,inputNum:(inputNum + apNum*2)],k)
pF.particleInitial(ini,100)
plt.figure()
for i in range(0,len(testingData)):
    move = testingData[i,:2]
    pF.particleMove(move)
    observe = testingData[i, inputNum:(inputNum + apNum*2)]
    pF.particleUpdate(observe)
    if pF.ifResample(50) == 1:
        pF.particleResample()
    pre = pF.getMean()[:2]
    # pre = GP(observe,4)
    # pre = pF.knn(level=observe,n=4)
    actual = testingData[i, 2:inputNum]
    KnnErr.append(pre - actual)

    # plt.clf()
    #
    # plt.axis([pF.origin[0] - 5, 60, pF.origin[1] - 10, 100])
    # plt.plot(pF.particles[:, 0], pF.particles[:, 1], 'ro')
    # plt.plot(actual[0], actual[1], 'go')
    # # plt.plot(pF.getMean()[0],pF.getMean()[1],'bo')
    # plt.plot(pF.GPknn(observe,1)[0], pF.GPknn(observe,1)[1], 'yo')
    # plt.pause(0.0001)


KnnErr =np.array(KnnErr)
np.savetxt("localization_error.csv",np.array(KnnErr),fmt='%f',delimiter=',',newline='\r\n')
errNorm = np.zeros([len(KnnErr),1])
for i in range(len(errNorm)):
    errNorm[i]=np.linalg.norm(KnnErr[i,:])
print(str(np.max(errNorm)))
print(str(np.mean(errNorm)))

print(str(np.min(errNorm)))
