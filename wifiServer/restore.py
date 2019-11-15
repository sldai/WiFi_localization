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
# modelPath="./model/svm/"
# dataAll = np.loadtxt('E:/WiFi/day1/3F/0 m per s.txt', dtype=float, delimiter=',')[:,1:]
# data=[]
# dataRun = np.loadtxt('E:/WiFi/day1/3F/1.5 m per s.txt', dtype=float, delimiter=',')[:,1:]
# color_iter = ['r','g','b','m']
#
# plt.figure()
# list=np.loadtxt("list.txt", dtype=float, delimiter=' ')
#
# ax = []
# inputN=2
# gap = 19


class Recover:
    def __init__(self, map_setting, raw_fingerprints):
        self.ap_num = map_setting['ap_num']
        self.lost_signal = map_setting['lost_signal']
        self.raw_fingerprints = raw_fingerprints.copy()
        self.recovered_result = raw_fingerprints.copy()
        self.recovered_fingerprints = np.zeros(raw_fingerprints.shape)
        self.recovered_fingerprints[:,:2] = raw_fingerprints[:,:2]
        self.svr = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0, tol=0.1, C=10, epsilon=10, shrinking=True,cache_size=1000, verbose=False, max_iter=-1)
        self.scaler = None

    def recover_process(self):
        self.scaler = StandardScaler().fit(self.raw_fingerprints[:,:2])
        for ap2 in range(self.ap_num):
            self.recover_pair(2+ap2, 2+ap2+self.ap_num)

    def recover_pair(self, ap2_index, ap5_index):
        data_train_index = (self.raw_fingerprints[:,ap2_index]!=self.lost_signal) & (self.raw_fingerprints[:,ap5_index]!=self.lost_signal)
        X = self.raw_fingerprints[data_train_index, :2]
        y = self.raw_fingerprints[data_train_index, ap5_index]-self.raw_fingerprints[data_train_index, ap2_index]
        if len(y) == 0:
            return
        self.svr.fit(self.scaler.transform(X), y)

        # recover 5G
        index_5G = (self.raw_fingerprints[:,ap2_index]!=self.lost_signal) & (self.raw_fingerprints[:,ap5_index]==self.lost_signal)
        X = self.raw_fingerprints[index_5G, :2]
        if len(X) > 0:
            y = self.raw_fingerprints[index_5G, ap2_index]+self.svr.predict(self.scaler.transform(X))
            self.recovered_fingerprints[index_5G, ap5_index] = y
            self.recovered_result[index_5G, ap5_index] = y
        # recover 2G
        index_2G = (self.raw_fingerprints[:, ap2_index] == self.lost_signal) & \
                   (self.raw_fingerprints[:,ap5_index] != self.lost_signal)
        X = self.raw_fingerprints[index_2G, :2]
        if len(X) > 0:
            y = self.raw_fingerprints[index_2G,ap5_index]-self.svr.predict(self.scaler.transform(X))
            self.recovered_fingerprints[index_2G, ap2_index] = y
            self.recovered_result[index_2G, ap2_index] = y

    def GetRecovered(self):
        return self.recovered_fingerprints.copy()

    def GetRaw(self):
        return self.raw_fingerprints.copy()

    def GetResult(self):
        return self.recovered_result.copy()











def Restore(dataAll, gap, inputN, num):
    ap2 = inputN + num
    ap5 = ap2+gap
    dataTemp= dataAll[dataAll[:,ap2]!=-100]
    dataTemp = dataTemp[dataTemp[:, ap5] != -100]

    index = (dataAll[:,ap5]!=-100) & (dataAll[:,ap2]==-100)
    dataTest = dataAll[index,:]
    train = dataTemp[:, :]


    X=np.c_[train[:,:inputN],train[:, ap5]]
    output = np.array(dataAll)
    # noise = np.zeros([len(output)])+1e-10
    # noise[index] = 1e-5
    # temp_plot = plt.figure().add_subplot(111, projection='3d')
    if len(X)>0 and len(dataTest):
        X_2D = X[:, :inputN]
        scaler = StandardScaler().fit(X_2D)

        X_2D = scaler.transform(X_2D)
        y=train[:,ap2]-train[:,ap5]

        rbf_svc = svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0, tol=0.1, C=10, epsilon=10, shrinking=True,
                          cache_size=1000, verbose=False, max_iter=-1)
        rbf_svc.fit(X_2D, y)


        X_pre = np.c_[dataTest[:,:inputN],dataTest[:, ap5]]
        X_2D_pre = X_pre[:,:inputN]

        pre=rbf_svc.predict(scaler.transform(X_2D_pre))
        #output[index, ap2] = output[index,ap5] + pre
        output[index, ap2] = -100

    return output[:,ap2], output[index, :]

# np.savetxt("csv/restore.csv", np.array(dataAll), fmt='%f', delimiter=',', newline='\r\n')
if __name__ == '__main__':
    # dataAll = np.loadtxt('E:/WiFi/day1/3F/0.5 m per s.csv', dtype=float, delimiter=',')[:, 1:]
    # map_setting = {'ap_num': 19, 'interval': 0.8, 'origin': [0.0, 0.0], 'lost_signal': -100}
    # recover_pro = Recover(map_setting=map_setting, raw_fingerprints = dataAll)
    # recover_pro.recover_process()
    # recovered = recover_pro.GetRecovered()
    # raw = recover_pro.GetRaw()
    #
    #
    # # plot raw fingerprints
    # for i in range(map_setting['ap_num']*2):
    #     plot_index = raw[:,2+i] != map_setting['lost_signal']
    #     X = raw[plot_index,:2]
    #     y = raw[plot_index,2+i]
    #     plot_index = recovered[:, 2 + i] != 0
    #     rX = recovered[plot_index,:2]
    #     ry = recovered[plot_index,2+i]
    #     ax = plt.figure().add_subplot(111, projection='3d')
    #     ax.scatter(X[:, 0], X[:, 1], y[:], c='r', label='mearsured')
    #     ax.scatter(rX[:, 0], rX[:, 1], ry[:], c='g', label='recovered')
    #     ax.legend()
    #
    # plt.show()
    data = np.loadtxt('E:/WiFi/day1/3F/0 m per s.csv', dtype=float, delimiter=',')[:, 1:]
    training_data, test_data = train_test_split(data, )



