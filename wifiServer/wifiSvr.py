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
dataRun = np.loadtxt('E:/WiFi/day1/3F/2 m per s.csv', dtype=float, delimiter=',')[:,1:]
color_iter = ['r','g','b','m']
list=np.loadtxt("list.txt", dtype=float, delimiter=' ')
for t in range(1):
    if t == 0:
        dataAll = np.loadtxt('E:/WiFi/day1/3F/0 m per s.txt', dtype=float, delimiter=',')[:, 1:]
        dataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/实验/static.csv", dtype=float, delimiter=',')
    elif t == 1:
        dataAll = np.loadtxt('E:/WiFi/day1/3F/0.5 m per s.txt', dtype=float, delimiter=',')[:, 1:]
    elif t == 2:
        dataAll = np.loadtxt('E:/WiFi/day1/3F/1 m per s.txt', dtype=float, delimiter=',')[:, 1:]
    elif t == 3:
        dataAll = np.loadtxt('E:/WiFi/day1/3F/1.5 m per s.txt', dtype=float, delimiter=',')[:, 1:]
    ax = []
    inputN = 2
    gap = -10
    error_3D_list = []
    error_2D_list = []
    error_run = []
    n=19
    for num in range(n,n+1):

        dataTemp= dataAll[dataAll[:,num+inputN]!=-100]
        dataTemp = dataTemp[dataTemp[:, num +gap+ inputN] != -100]


        testChoice = range(0, len(dataTemp), 4)
        dataTest = dataTemp[testChoice,:]
        trainSet = dataTemp[:, :]
        trainSet[testChoice, 0] = 2333
        train = trainSet[trainSet[:, 0] != 2333]



        X=np.c_[train[:,:inputN],train[:, gap+num + inputN]]

        temp_plot = plt.figure().add_subplot(111, projection='3d')
        if len(X)>0:
            X_2D = X[:, :inputN]
            scaler = StandardScaler().fit(X_2D)

            X_2D = scaler.transform(X_2D)
            y=train[:,num+inputN]-train[:,num+inputN+gap]
            grid = GridSearchCV(svm.SVR(kernel='rbf',cache_size=1000),param_grid={"C":np.arange(0.1,10,1), "gamma":[0.9],'epsilon':range(10,16)}, cv=4)
            # grid.fit(X,y)
            # print('The best parameters are %s with a score of %0.2f' % (grid.best_params_, grid.best_score_))

            rbf_svc = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0, tol=0.1, C=10, epsilon=10, shrinking=True,
                              cache_size=1000, verbose=False, max_iter=-1)
            rbf_svc.fit(X_2D, y)
            dataPre = dataAll[dataAll[:,num+inputN]==-100]
            dataPre = dataTemp[dataTemp[:, num +gap+ inputN] != -100]


            X_pre = np.c_[dataTest[:,:inputN],dataTest[:, gap+num + inputN]]
            X_2D_pre = X_pre[:,:inputN]
            pre=rbf_svc.predict(scaler.transform(X_2D_pre))
            error_2D = (pre-(dataTest[:,num+inputN]-dataTest[:,num +gap+ inputN])).tolist()
            error_2D_list+=error_2D


            temp_plot.scatter(dataTest[:,0], dataTest[:,1], pre+dataTest[:,num +gap+ inputN], c='g')
            temp_plot.scatter(dataTest[:, 0], dataTest[:, 1], (dataTest[:,num+inputN]), c='b')
            temp_plot.scatter(train[:, 0], train[:, 1],  train[:,num+inputN], c='r')
            temp_plot.set_zlabel('Z')  # 坐标轴
            temp_plot.set_ylabel('Y')
            temp_plot.set_xlabel('X')
            temp_plot.legend(['predict','test','train'])



    plt.figure()
    plt.hist(abs(np.array(error_2D_list)),50, normed=1, histtype='step', color=color_iter[t], alpha=1, cumulative=True, rwidth=0.8)
    print(np.mean(abs(np.array(error_2D_list))))

font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,}
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(['with sojourn','0.5 m/s','1 m/s','1.5 m/s'],prop=font1,loc = 'lower center')
plt.xlabel('Error (dBm)',font1)
plt.ylabel('CDF',font1)
plt.show()

