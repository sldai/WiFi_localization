#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
import random as rand
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import itertools
modelPath="./model/svm/"

data=[]
data1 = np.loadtxt('E:/WiFi/day1/3F/2 m per s.csv', dtype=float, delimiter=',')[:,1:]
data2 = np.loadtxt('E:/WiFi/day2/2 m per s.txt', dtype=float, delimiter=',')[:,1:]
data3 = np.loadtxt('E:/WiFi/day3/2 m per s.txt', dtype=float, delimiter=',')[:,1:]
data4 = np.loadtxt('E:/WiFi/day4/2 m per s.txt', dtype=float, delimiter=',')[:,1:]
color_iter = ['r','g','b','m']
list=np.loadtxt("list.txt", dtype=float, delimiter=' ')

ax = []
inputN = 2
apNum = 19


def RSS_to_SSD(apNum, RSS):
    SSD = []
    # 2G SSD
    for i in range(apNum - 1):
        for j in range(i + 1, apNum):
            if RSS[i] != -100 or RSS[j] != -100:
                SSD.append(-100)
            else:
                SSD.append(RSS[i] - RSS[j])

    # 5G SSD
    for i in range(apNum, 2 * apNum - 1):
        for j in range(i + 1, 2 * apNum):
            if RSS[i] != -100 or RSS[j] != -100:
                SSD.append(-100)
            else:
                SSD.append(RSS[i] - RSS[j])

    return np.array(SSD)

for num in range(apNum,apNum*2):
    temp_plot = plt.figure().add_subplot(111, projection='3d')
    ap2 = inputN + num
    ap5 = ap2+apNum
    X=data1[:,:inputN]
    y=data1[:,ap2]
    temp_plot.scatter(X[:,0],X[:,1],y,'r')

    X = data2[:, :inputN]
    y = data2[:, ap2]
    temp_plot.scatter(X[:, 0], X[:, 1], y,'g')

    X = data3[:, :inputN]
    y = data3[:, ap2]
    temp_plot.scatter(X[:, 0], X[:, 1], y,'b')

    X = data4[:, :inputN]
    y = data4[:, ap2]
    temp_plot.scatter(X[:, 0], X[:, 1], y,'m')




    temp_plot.set_zlabel('Z')  # 坐标轴
    temp_plot.set_ylabel('Y')
    temp_plot.set_xlabel('X')
    temp_plot.legend(['test','predict'])


plt.show()

