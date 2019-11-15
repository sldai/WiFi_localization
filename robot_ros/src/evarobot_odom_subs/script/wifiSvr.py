# -- coding: utf-8 --
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
import random as rand
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import math as mt
modelPath="./model/svm/"
data = np.loadtxt("2018-04-11 20_20_28.txt", dtype=float, delimiter=',')
dataWithout100=[]
for num in range(20):
    temp=[]
    for i in range(len(data)):
        if data[i,2+num]!=-100:
            temp.append([data[i,0], data[i,1], data[i,2 + num]])

    dataWithout100.append(temp)

ax = []
for num in range(20):
    tempArray=np.array(dataWithout100[num])
    tempModel = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=10, epsilon=0.1, shrinking=True,
                   cache_size=200, verbose=False, max_iter=-1)
    tempModel.fit(tempArray[:,:2],tempArray[:,2])
    joblib.dump(tempModel, modelPath + "ap" + str(num) + ".pkl")
    result=tempModel.predict(tempArray[:,:2])
    ax.append(plt.figure().add_subplot(111, projection='3d'))
    ax[num].scatter(tempArray[:,0],tempArray[:,1],tempArray[:,2],c='r')
    ax[num].scatter(tempArray[:,0], tempArray[:,1], result[:], c='g')
    ax[num].set_zlabel('Z')  # 坐标轴
    ax[num].set_ylabel('Y')
    ax[num].set_xlabel('X')
    ax[num].legend(['test','predict'])
plt.show()

