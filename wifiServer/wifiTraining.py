import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn import svm
from sklearn.model_selection import train_test_split
import random as rand
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import math as mt
import scipy.io as scio
from nn_predict import NN_predict
modelPath="./model/svm/"
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/complete.csv", dtype=float, delimiter=',')
dataWithout100=[]
default=-90
data[data[:,:]==-100] = default
for num in range(20):
    temp=[]
    for i in range(len(data)):
        if data[i,2+num]!=-100:
            temp.append([data[i,0], data[i,1], data[i,2 + num]])

    dataWithout100.append(temp)

lastData = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-04-11 20_20_28.txt", dtype=float, delimiter=',')

wifiNum=20

trainingData, testingData = train_test_split(data, test_size=0.2)

length = len(testingData)
y = []
clf = []
ax = []
X = trainingData[:, :2]
pp=[]
for i in range(wifiNum):
    pp.append(NN_predict("alone/model_1/model" + str(i + 1) + "/"))
    print('OK!', i)
jobArray=[]
for i in range(0, wifiNum):
    jobArray.append(joblib.load("6b/model/svm/" + "ap" + str(i) + ".pkl"))  # 载入学习模型
resultArray=[]
grid = scio.loadmat("6b"+"/grid/" + 'gridno-100.mat')
grid = grid['grid']
row = grid.shape[0]
col = grid.shape[1]
origin = scio.loadmat("6b"+"/grid/" +  'origin.mat')
origin = origin['origin'][0]
#resultArray = np.array(resultArray)
ax = []
for i in range(0, wifiNum):
    y.append(trainingData[:, 2 + i])
    temp = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.8, epsilon=0.1, shrinking=True,
              cache_size=200, verbose=False, max_iter=-1)
    clf.append(temp)
    clf[i].fit(X, y[i])
    #joblib.dump(clf[i],modelPath+"ap"+str(i)+".pkl")
    ax.append(plt.figure().add_subplot(111, projection='3d'))
    #ax[i].scatter(data[:, 0], data[:, 1], data[:, 2 + i], c='y')
    tempArray=np.array(dataWithout100[i])
    # result=pp[i].predict(tempArray[:,:2])#dnn
    # tempre=result[:,0]-tempArray[:, 2]
    # tempre.tolist()

    result=jobArray[i].predict(tempArray[:,:2])#svr
    tempre = result[:] - tempArray[:, 2]
    resultArray.extend(tempre)
    tempre.tolist()


    # result=[]
    # for p in range(len(tempArray)):
    #     tempx = int(round(tempArray[p, 0] - origin[0]))
    #     tempy = int(round(tempArray[p, 1] - origin[1]))
    #     tempResult=grid[tempy,tempx,i]
    #     result.append(tempResult)
    # result=np.array(result)
    # tempre = result[:] - tempArray[:, 2]
    # resultArray.extend(tempre)
    # tempre.tolist()#discrete

    #result=result[:,0]-tempArray[:, 2 ]
    ax[i].scatter(tempArray[:, 0], tempArray[:, 1], tempArray[:, 2 ], c='r')
    ax[i].scatter(tempArray[:, 0], tempArray[:, 1], result[:], c='g')
    # for j in range(0, len(data)):
    #     if data[j, 2 + i]!=-100:
    #         pre = pp.predict(data[j, :2])[0][i] - data[j, 2 + i]
    #         ax[i].scatter(data[j, 0], data[j, 1], pre, c='r')



    # print( "\n",i + 1,":")
    # for j in range(0, length):
    #     if testingData[j,2+i]!=-100:
    #         result = clf[i].predict([testingData[j, :2]])
    #         ax[i].scatter(testingData[j, 0], testingData[j, 1], result, c='g')
    #         print(result - testingData[j, 2 + i])
    ax[i].set_zlabel('Z')  # 坐标轴
    ax[i].set_ylabel('Y')
    ax[i].set_xlabel('X')
    ax[i].legend(['NowData', 'LastData', 'predictVar'])
plt.show()
np.savetxt("MapSvrErr.csv",np.array(resultArray),fmt='%f',delimiter=',',newline='\r\n')