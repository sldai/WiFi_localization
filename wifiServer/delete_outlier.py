import time
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.externals import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, Matern, ConstantKernel, RBF, RationalQuadratic
from sklearn.model_selection import train_test_split
from mpl_toolkits.mplot3d import Axes3D
from outliers import smirnov_grubbs as grubbs
from scipy import stats
from sklearn.preprocessing import StandardScaler

def standarize_residue(residue, variance):
    return residue/variance

interval = 0.8
ap_num = 19
dataRaw = np.loadtxt("E:/WiFi/day1/3F/0.5 m per s.csv", dtype=float, delimiter=',')[:, 1:]
dataResurvey = np.loadtxt("E:/WiFi/day1/3F/1 m per s.csv", dtype=float, delimiter=',')[:,1:]
data_sojourn = np.loadtxt("E:/WiFi/day1/3F/0 m per s.csv", dtype=float, delimiter=',')[:836, 1:]
data_test = np.loadtxt("E:/WiFi/day1/3F/2 m per s.csv", dtype=float, delimiter=',')[:, 1:]
grid = np.loadtxt("survey_results/3F_corridor/candidate.csv", dtype=float, delimiter=',')[:]
#grid = np.array(dataAll[:,:2])



def resurvey(data):
    # each ap has its fingerprint list
    AP_list = []
    AP_missed_list = []
    AP_outlier_list = []
    for i in range(ap_num*2):
        fingerprints = np.column_stack((data[:,:2], data[:,2+i]))
        AP_list.append(fingerprints)
        AP_missed_list.append([])
        AP_outlier_list.append([])

    max_resurvey_time = 1
    for resurvey_time in range(max_resurvey_time): # the extra 1 is used to delete outliers in last resurvey
        resurvey_point = []
        for ap in range(ap_num*2):
            traning_data = AP_list[ap]
            AP_missed_list[ap].extend(traning_data[traning_data[:,2]==-100,:].tolist())
            traning_data = traning_data[traning_data[:,2]!=-100,:]
            if len(traning_data) <= 100:
                continue

            kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1)
            gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
            X = traning_data[:,:2]
            y = traning_data[:,2]

            scaler = StandardScaler().fit(X)

            outliers = []
            cnt=0
            while True:
                gpr.fit(scaler.transform(X), y)
                # print(gpr.kernel_.k2.noise_level)
                noise_std = math.sqrt(gpr.kernel_.k2.noise_level)
                y_gpr, y_std = gpr.predict(scaler.transform(X), return_std=True)
                residue = (y - y_gpr)
                # residue = abs(residue) / noise_std
                # residue = residue.tolist()

                residue = ([abs(standarize_residue(residue[i], std)) for i, std in enumerate(y_std)])
                if max(residue)<2:
                    break
                index = residue.index(max(residue))

                # index = grubbs.test_once(residue)
                if index is None:
                    break

                outlier = np.array([X[index, 0], X[index, 1], y[index]])
                outliers.append(outlier)
                outlier_position = [round(outlier[0]/interval)*interval, round(outlier[1]/interval)*interval]
                if outlier_position not in resurvey_point:
                    resurvey_point.append(outlier_position)
                X = np.delete(X, index, axis=0)
                y = np.delete(y, index, axis=0)
                traning_data = np.delete(traning_data, index, axis=0)

                cnt+=1

            AP_list[ap] = traning_data
            AP_outlier_list[ap].extend(outliers)
            print(cnt)

            # ax = plt.figure().add_subplot(111, projection='3d')
            # ax.set_title(str(ap))
            # ax.scatter(X[:, 0], X[:, 1], y[:], c='r', label = 'mearsured')
            # ax.scatter(X[:, 0], X[:, 1], y_gpr[:], c='g', label = 'estimated')
            # if cnt > 0:
            #     outliers = np.array(outliers)
            #     ax.scatter(outliers[:, 0], outliers[:, 1], outliers[:, 2], c='b', label = 'outlier')
            # ax.legend()

        # last loop only used to delete outliers
        # if resurvey_time == max_resurvey_time:
        #     for i in range(ap_num*2):
        #         AP_list[i] = np.array(AP_list[i])
        #         AP_outlier_list[i] = np.array(AP_outlier_list[i])
        #         AP_missed_list[i] = np.array(AP_missed_list[i])
        #     break
        resurvey_point = np.array(resurvey_point)
        print("resurvey points are "+str(len(resurvey_point)))

        extra_fingerprints = get_resurveyed_data(resurvey_point)
        print("extra fingerprints are " + str(len(extra_fingerprints)))
        np.savetxt("resurvey/resurvey_"+str(resurvey_time)+".csv", np.array(extra_fingerprints), fmt='%f', delimiter=',', newline='\r\n')
        # for i in range(ap_num*2):
        #     fingerprints = np.column_stack((extra_fingerprints[:,:2], extra_fingerprints[:,2+i]))
        #     AP_list[i] = np.row_stack((AP_list[i],fingerprints))
    # plt.show()
    return extra_fingerprints




def get_resurveyed_data(resurvey_list):
    extra_fingerprint_list = []
    for point in resurvey_list:
        for fingerprint in data_sojourn:
            if np.linalg.norm(fingerprint[:2] - point) < interval/2:
                extra_fingerprint_list.append(fingerprint)
    return np.array(extra_fingerprint_list)

def only_remove_outliers(training_data):
    X = training_data[:, :2]
    y = training_data[:, 2]
    kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1)
    gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
    while True:
        if len(X) <= 0:
            break
        gpr.fit(X, y)
        # print(gpr.kernel_.k2.noise_level)
        noise_std = math.sqrt(gpr.kernel_.k2.noise_level)
        y_gpr, y_std = gpr.predict(X, return_std=True)
        residue = (y - y_gpr)
        # residue = abs(residue) / noise_std
        # residue = residue.tolist()

        residue = ([abs(standarize_residue(residue[i], std)) for i, std in enumerate(y_std)])
        if max(residue) < 3:
            break
        index = residue.index(max(residue))

        # index = grubbs.test_once(residue)
        if index is None:
            break
        X = np.delete(X, index, axis=0)
        y = np.delete(y, index, axis=0)
    return np.column_stack((X, y))

def get_GP_model(training_data, grid):
    gridMean = np.array(grid)
    gridStd = np.array(grid)
    input_num = 2
    scaler = StandardScaler().fit(training_data[:, :input_num])
    for ap in range(0, ap_num*2):
        training_data_without_outliers = training_data
        kernel = 1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) \
                 + WhiteKernel(noise_level=1.0)
        gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
        X = training_data_without_outliers[:,:2]
        y = training_data_without_outliers[:, 2+ap]
        gpr.fit(scaler.transform(X), y)
        # predict
        y_gpr, y_std = gpr.predict(scaler.transform(grid), return_std=True)
        # if ap == 0:
        #     ax = plt.figure().add_subplot(111, projection='3d')
        #     ax.scatter(X[:,0], X[:,1], y[:], c='r', label = 'measured')
        #     ax.scatter(grid[:, 0], grid[:, 1], y_gpr[:], c='g', label='predicted')
        gridMean = np.column_stack((gridMean,y_gpr))
        gridStd = np.column_stack((gridStd,y_std))
    # plt.show()
    return gridMean, gridStd

lost_signal = -90
import math as mt
from copy import deepcopy
def local_err(testingdata, gpr, std, type):

    def GP(ob, n, type):
        nnlist = []
        for i in range(len(gpr)):
                x = gpr[i,0]
                y = gpr[i,1]
                p = 1
                dis = 0
                pro=0
                ap_picked = [3,4,5,6,7]
                ap_picked_tmp = deepcopy(ap_picked)
                for o in ap_picked:
                    ap_picked_tmp.append(o+ap_num)
                ap_picked = ap_picked_tmp
                # ap_picked = range(2*ap_num)
                for num in ap_picked:
                    if ob[num] != lost_signal:
                        u = gpr[i,2+num]
                        sigma = std[i,2+num]
                        p *= mt.exp(-(u - ob[num]) ** 2 / (2 * (sigma) ** 2)) / sigma * 1000
                        dis += (u - ob[num])**2
                dis = dis**0.5
                if type == "knn":
                    pro = 1/dis
                elif type == "bayes":
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

    err_list = []
    for test_point in testingdata:
        ob = test_point[2:]
        mean = GP(ob, 4, type)
        err = np.linalg.norm(mean-test_point[:2])
        err_list.append(err)

    print('mean error = ' + str(sum(err_list)/len(err_list)))
    print('max error = ' + str(max(err_list)))
    return err_list


if __name__ == '__main__':
   # extra_fingerprints = resurvey()
   dataSurvey = np.loadtxt("survey_results/3F_corridor/sojourn/survey0.csv", dtype=float, delimiter=',')[:,1:]
   dataSurvey[dataSurvey[:,:]==-100] = lost_signal
   dataTest = np.loadtxt("survey_results/3F_corridor/test2/survey0.csv", dtype=float, delimiter=',')[:,1:]
   dataTest[dataTest[:, :] == -100] = lost_signal
   GP_mean, GP_std = get_GP_model(dataSurvey, grid)
   # np.savetxt("survey_results/3F_corridor/fingerprint_map/recover1_mean.csv", np.array(GP_mean), fmt='%f', delimiter=',', newline='\r\n')
   # np.savetxt("survey_results/3F_corridor/fingerprint_map/recover1_std.csv", np.array(GP_std), fmt='%f', delimiter=',', newline='\r\n')
   err_result = local_err(dataTest, GP_mean, GP_std, "knn")
   np.savetxt("survey_results/3F_corridor/local_result/pure_wifi/sojourn_knn.csv", np.array(err_result), fmt='%f', delimiter=',', newline='\r\n')
   # plt.show()