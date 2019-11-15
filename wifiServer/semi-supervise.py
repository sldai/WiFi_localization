import numpy as np
import matplotlib.pyplot as plt
from sklearn.semi_supervised import label_propagation
from sklearn.datasets import make_circles
from sklearn import svm
import math

EdgeAndCorner = np.loadtxt("E:/project/PycharmProjects/wifiServer/6b/map/edge and corner.txt", dtype=float,
                           delimiter=',')


def belong(raw):
    belongData = []
    for i in range(len(raw)):
        xc, yc, theta, ro = 0, 0, 0, 0
        for j in range(len(EdgeAndCorner)):
            if raw[i, 0] > EdgeAndCorner[j, 0] and raw[i, 1] > EdgeAndCorner[j, 1] and raw[i, 0] < EdgeAndCorner[
                j, 2] and raw[i, 1] < EdgeAndCorner[j, 3]:
                xc = (EdgeAndCorner[j, 0] + EdgeAndCorner[j, 2]) / 2
                yc = (EdgeAndCorner[j, 1] + EdgeAndCorner[j, 3]) / 2
                theta = EdgeAndCorner[j, 6]
                ro = EdgeAndCorner[j, 5]
                index = j
                break
        belongData.append([raw[i, 0], raw[i, 1], raw[i, 2], index])

    return np.c_[np.array(belongData), raw[:, 3:]]


def maxmin(belongdata):
    maxminarray = np.ones([len(EdgeAndCorner), 10, 2]) * -100
    for j in range(len(EdgeAndCorner)):
        tempdata = belongdata[belongdata[:, 3] == j, :]
        for i in range(10):
            tempdatai = tempdata[tempdata[:, inputNum + i] != -100, inputNum + i]
            if len(tempdatai) > 0:
                tempmax = max(tempdatai)
                tempmin = min(tempdatai)
                maxminarray[j, i, 0] = tempmax
                maxminarray[j, i, 1] = tempmin
    return maxminarray


def suppleMax(X, maxminarray, APnum):
    temp = np.zeros([len(X), 2])
    for i in range(len(X)):
        temp[i, 0] = maxminarray[int(X[i, 3]), APnum, 0]
        temp[i, 1] = maxminarray[int(X[i, 3]), APnum, 1]
    return np.c_[X[:, :2], X[:, 4:]]

def giveInterval(array):
    cluster = 10
    sortarray = array[array[:] != -100]
    sortarray = np.sort(sortarray)
    totalNum = len(array)
    gap = int(round(totalNum / cluster))
    intervalList = np.zeros([1+cluster])
    intervalList[0] = -95.1
    intervalList[0] = -17
    for i in range(1, cluster):
        intervalList[i] = sortarray[i * gap - 1]
    return intervalList
def labeling(array,intervalList):
    cluster = 10
    sortarray = array[array[:] != -100]
    totalNum = len(array)

    for i in range(totalNum):
        if array[i] == -100:
            array[i] = -1
            continue
        # if array[i]>=intervalList[-1]:
        #     array[i]=cluster-1
        #     continue
        for j in range(cluster):
            if array[i]>intervalList[j] and array[i]<=intervalList[j+1]:
                array[i]=j
                break

    return array
def delabel(array):
    RSSI = np.array(array)
    for i in range(len(array)):
        RSSI[i]=(intervalList[array[i]]+intervalList[array[i]+1])/2
    return

# dataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-06-30 21_42_19.txt", dtype=float, delimiter=',')
# dataWithEdge = belong(dataAll)
# np.savetxt("E:/WiFi/实验室6楼/wifiData/2018-06-30 21_42_19.csv",dataWithEdge,fmt='%f',delimiter=',',newline='\r\n')
# dataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-06-30 22_12_19.txt", dtype=float, delimiter=',')
# dataWithEdge = belong(dataAll)
# np.savetxt("E:/WiFi/实验室6楼/wifiData/2018-06-30 22_12_19.csv",dataWithEdge,fmt='%f',delimiter=',',newline='\r\n')
interval = 10
inputNum = 2

dataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/raw.csv", dtype=float, delimiter=',')
# dataAll[:,2]=np.round(dataAll[:,2]/(math.pi*0.5))
# dataAll = np.delete(dataAll, 2, 1)
# dataAll=belong(dataAll)
maxminarray = maxmin(dataAll)

testdataAll = np.loadtxt("E:/WiFi/实验室6楼/wifiData/test.csv", dtype=float, delimiter=',')[:800]
# testdataAll = np.delete(testdataAll, 2, 1)
# testdataAll=belong(testdataAll)
for Ap in range(10):
    testAP = inputNum + Ap
    testAPBand = testAP + interval
    # ignore the default RSSI
    data = dataAll[dataAll[:, testAPBand] != -100, :]
    data = data[data[:, testAP] != -100, :]
    intervalList = giveInterval(data[:,testAP])
    dataNotUse = dataAll[dataAll[:, testAPBand] == -100, :]

    dataPredict = dataAll[dataAll[:, testAPBand] != -100, :]
    dataPredict = dataPredict[dataPredict[:, testAP] == -100, :]
    dataPredictX = np.c_[dataPredict[:, :inputNum], dataPredict[:, testAPBand]]

    semidata = dataAll[dataAll[:, testAPBand] != -100, :]
    # length
    datalength = len(data)
    # testing data
    testdata = testdataAll[testdataAll[:, testAPBand] != -100, :]
    testdata = testdata[testdata[:, testAP] != -100, :]
    testdataX = np.c_[testdata[:, :inputNum], testdata[:, testAPBand]]
    testlabel = labeling(testdata[:, testAP],intervalList)

    # labeling  semi use
    # restore
    y=int(round((semidata[:,testAP]+95)/10))

    X=np.c_[semidata[:,:inputNum],semidata[:,testAPBand]]
    # Learn with LabelSpreading

    label_spread = label_propagation.LabelSpreading(kernel='rbf', gamma=0.1,alpha=0.15)
    label_spread.fit(X, y)

    output_labels = label_spread.transduction_
    semidata[:, testAP] = label_spread.transduction_[:]*10-95+5
    dataAll=np.r_[semidata,dataNotUse]
    print(testAP)
    figure=plt.figure().add_subplot(111)
    # err
    output_labels = label_spread.predict(testdataX)
    err=np.mean((output_labels[:]*10-95+5-testdata[:,testAP])**2)
    maxerr=np.max(abs(output_labels[:]*10-95+5-testdata[:,testAP]))
    print(str(maxerr))


    # compare with svm
    # labeling  supervise use

    # compare with svr

    # y = data[:, testAP]
    #
    # X = np.c_[data[:, :inputNum], data[:, testAPBand]]
    # rbf_svc = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=10, epsilon=0.1, shrinking=True,
    #                cache_size=200, verbose=False, max_iter=-1)
    # rbf_svc.fit(X,y)
    # svr=rbf_svc.predict(testdataX)
    #
    # err=np.mean((svr-testdata[:,testAP])**2)
    # maxerr=np.max(abs(svr-testdata[:,testAP]))
    # print(maxerr)

np.savetxt("E:/project/PycharmProjects/wifiServer/csv/restore data.csv", dataAll, fmt='%f', delimiter=',',
           newline='\r\n')
plt.show()
