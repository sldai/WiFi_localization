import numpy as np
from numpy import argsort
import matplotlib.pyplot as plt
from sklearn import svm
import random as rand
from mpl_toolkits.mplot3d import Axes3D
import xlrd
import math as mt
import scipy.io as scio
from sklearn.externals import joblib
from readMap import read_pgm
from readMap import read_ros_map
import yaml
from wifi_eval import evaluate
from nn_predict import NN_predict
import math
import cv2


class particleFilter:
    def __init__(self, apNum, modelType, Path, localType = "bayes"):
        self.apNum = apNum
        self.model = []
        self.modelType = modelType
        self.path = Path
        self.localType = localType
        # load grid parameter
        grid = scio.loadmat(Path + "/grid/0/" + 'grid.mat')
        origin = scio.loadmat(Path + "/grid/0/" + 'origin.mat')
        self.grid = grid['grid']
        self.origin = origin['origin'][0]
        # load map
        f = open(Path + "/map/mymap.yaml")
        temp = yaml.load(f)
        self.resolution = temp['resolution']
        self.map_origin = temp['origin']
        map = temp['image']
        # map = open(Path+"/map/" + map, 'rb')
        self.map = read_ros_map(Path + "/map/" + 'mymap.pgm')
        # load machine learning
        if self.modelType == "svm":
            for i in range(0, self.apNum):
                temp = joblib.load(Path + "/model/svm/" + "ap" + str(i) + ".pkl")  # 载入学习模型
                self.model.append(temp)
        elif self.modelType == "dnn":
            self.model = []
            for i in range(0, self.apNum):
                self.model.append(NN_predict("alone/model_1/model" + str(i + 1) + "/"))
        elif self.modelType == 'GP':
            self.gpr = np.loadtxt("survey_results/3F_corridor/fingerprint_map/sojourn_mean.csv", dtype=float, delimiter=',')
            self.std = np.loadtxt("survey_results/3F_corridor/fingerprint_map/sojourn_std.csv", dtype=float, delimiter=',')
            # for ap in range(self.apNum):
            #     meanMap = np.ones([int(len(self.map) / 10), int(len(self.map[0,:]) / 10)])*-100
            #     stdMap = np.ones([int(len(self.map) / 10), int(len(self.map[0,:]) / 10)])
            #     for i in range(len(self.gpr)):
            #         x = self.gpr[i, 0]
            #         y = self.gpr[i, 1]
            #         x_pixel = int(round(mt.floor((x - self.map_origin[0]) / (10*self.resolution))))
            #         y_pixel = int(round(mt.floor((y - self.map_origin[1]) / (10*self.resolution))))
            #         meanMap[y_pixel, x_pixel] = (round(self.gpr[i, 2 + ap]))
            #         stdMap[y_pixel, x_pixel] = (round(self.std[i, 2 + ap]))
            #     self.model.append(meanMap)
            #     self.model.append(stdMap)
        elif self.modelType == "knn":
            self.model = None
        elif self.modelType == 'probability':
            self.model = None
        elif self.modelType == 'Nearest':
            self.model = None

    def read_ros_map(self, pgm_map):
        mapData = read_pgm(pgm_map)
        mapData = np.array(mapData)
        mapData = mapData[::-1]
        return mapData

    def RSS_to_SSD(self, RSS):
        SSD = []
        # 2G SSD
        for i in range(self.apNum-1):
            for j in range(i+1,self.apNum):
                if RSS[i]==-100 or RSS[j]==-100:
                    SSD.append(-100)
                else:
                    SSD.append(RSS[i] - RSS[j])

        # 5G SSD
        for i in range(self.apNum, 2*self.apNum - 1):
            for j in range(i + 1, 2*self.apNum):
                if RSS[i] == -100 or RSS[j] == -100:
                    SSD.append(-100)
                else:
                    SSD.append(RSS[i] - RSS[j])

        return np.array(SSD)

    def knn_SSD(self, level, n):

        nnlist = []
        row = self.grid.shape[0]
        col = self.grid.shape[1]
        for i in range(row):
            for j in range(col):
                if self.grid[i, j, 0] != 0:
                    dis = 0
                    finger_SSD = self.RSS_to_SSD(level)
                    map_SSD = self.RSS_to_SSD(self.grid[i][j][:])
                    for num in range(len(map_SSD)):
                        if finger_SSD[num] != -100:
                            dis += (finger_SSD[num] - map_SSD[num]) ** 2
                    pro = 1.0 / (dis ** 0.5 + 0.01)
                    nnlist.append([j, i, pro])
        nnlist = np.array(nnlist)
        # nnlist[:, 0]+=self.origin[0]
        # nnlist[:, 1] += self.origin[1]
        # np.savetxt("candidate.csv", nnlist[:,:2], fmt='%f', delimiter=',', newline='\r\n')
        mean = [self.origin[0], self.origin[1]]
        nnlist = nnlist[np.lexsort(-nnlist.T)]
        nnlist = nnlist[:n]
        nnlist[:, 2] = nnlist[:, 2] / sum(nnlist[:, 2])
        for i in range(n):
            mean += nnlist[i, :2] * nnlist[i, 2]
        return mean

    def SSD_var(self, var):
        SSD = []
        # 2G SSD
        for i in range(self.apNum - 1):
            for j in range(i + 1, self.apNum):
                    SSD.append(var[i]**2 + var[j]**2)

        # 5G SSD
        for i in range(self.apNum, 2 * self.apNum - 1):
            for j in range(i + 1, 2 * self.apNum):
                    SSD.append(var[i]**2 + var[j]**2)

        return np.array(SSD)
    def knn(self, level, n):
        nnlist = []
        row = self.grid.shape[0]
        col = self.grid.shape[1]
        for i in range(row):
            for j in range(col):
                if self.grid[i, j, 0] != 0:
                    dis = 0
                    for num in range(self.apNum*2):
                        if level[num] != -100:
                            dis += (level[num] - self.grid[i][j][num]) ** 2
                    pro = 1.0 / (dis ** 0.5 + 0.01)
                    nnlist.append([j, i, pro])
        nnlist = np.array(nnlist)
        # nnlist[:, 0]+=self.origin[0]
        # nnlist[:, 1] += self.origin[1]
        # np.savetxt("candidate.csv", nnlist[:,:2], fmt='%f', delimiter=',', newline='\r\n')
        mean = [self.origin[0], self.origin[1]]
        nnlist = nnlist[np.lexsort(-nnlist.T)]
        nnlist = nnlist[:n]
        nnlist[:, 2] = nnlist[:, 2] / sum(nnlist[:, 2])
        for i in range(n):
            mean += nnlist[i, :2] * nnlist[i, 2]
        return mean

    def GPknn(self, ob, n):
        nnlist = []
        finger_SSD = self.RSS_to_SSD(ob)
        for i in range(len(self.gpr)):
            x = self.gpr[i, 0]
            y = self.gpr[i, 1]
            p = 1
            dis=0

            for num in range(2*self.apNum):
                # if num==1:
                #     continue
                if ob[num] != -90:
                    u = self.gpr[i, 2 + num]
                    sigma = self.std[i, 2 + num]
                    p *= mt.exp(-(u - ob[num]) ** 2 / (2 * (sigma) ** 2)) / sigma * 10*100
                    dis += (ob[num] - u) ** 2

            # map_SSD = self.RSS_to_SSD(self.gpr[i, 2:])
            # sigma = self.SSD_var(self.std[i, 2:])
            # for num in range(len(map_SSD)):
            #     # if num==1:
            #     #     continue
            #
            #
            #     if finger_SSD[num] != -100:
            #
            #         #p *= mt.exp(-(map_SSD[num] - finger_SSD[num]) ** 2 / (2 * (sigma[num]) )) / (sigma[num]**0.5) * 10*100
            #         dis += (map_SSD[num] - finger_SSD[num]) ** 2
            pro = None
            if self.localType == "bayes":
                pro = p
                if pro==0:
                    pro=0.0001
            elif self.localType == "knn":
                pro = 1.0 / (dis ** 0.5 + 0.01)
            nnlist.append([x, y, pro])
        nnlist = np.array(nnlist)
        mean = [0, 0]
        nnlist = nnlist[np.lexsort(-nnlist.T)]
        nnlist = nnlist[:n]
        nnlist[:, 2] = nnlist[:, 2] / sum(nnlist[:, 2])
        for i in range(n):
            mean += nnlist[i, :2] * nnlist[i, 2]
        return mean

    def particleInitial(self, beginPoint, num):
        particles = []
        self.n = num
        for i in range(0, self.n):
            particles.append([beginPoint[0] + rand.uniform(-3, 3), beginPoint[1] + rand.uniform(-3, 3), 1.0 / self.n,
                              rand.uniform(0, 2 * math.pi)])
        self.particles = np.array(particles)
        return self.particles

    def particleMove(self, move):
        for i in range(0, self.n):
            self.particles[i, :2] += move + [rand.uniform(1, -1), rand.uniform(1, -1)]

        self.particleAbandon()
        return 0

    def particleMoveRobot(self, move):
        for i in range(0, self.n):
            self.particles[i, 0] += move[0] * math.cos(self.particles[i, 3]) - move[1] * math.sin(
                self.particles[i, 3]) + rand.uniform(-0.01, 0.01)
            self.particles[i, 1] += move[0] * math.sin(self.particles[i, 3]) + move[1] * math.cos(
                self.particles[i, 3]) + rand.uniform(-0.01, 0.01)
            self.particles[i, 3] += move[2] + rand.uniform(-0.01, 0.01)

    def particleUpdate(self, observe):
        total = 0
        if self.modelType == 'GP':
            centerPredict = self.GPknn(observe, n=4)
        elif self.modelType == 'knn':
            centerPredict = self.knn_SSD(observe, n=3)
        for i in range(0, self.n):
            dis = 0
            pro = 0
            if self.modelType == 'svm':
                for j in range(0, self.apNum):
                    if observe[j] != -100:
                        temp_clf = self.model[j]
                        predict = temp_clf.predict([self.particles[i, :2]])
                        dis = dis + (predict - observe[j]) ** 2
                pro = mt.exp(-dis / 10.0 / 10.0 / 2)
            elif self.modelType == 'dnn':
                for j in range(0, self.apNum):
                    if observe[j] != -100:
                        dis = dis + (self.model[j].predict([self.particles[i, :2]])[0, 0] - observe[j]) ** 2
                pro = mt.exp(-dis / 10.0 / 10.0 / 2)

            elif self.modelType == 'GP':
                # p=1
                # x_pixel = int(round(mt.floor((self.particles[i, 0] - self.map_origin[0]) / (10*self.resolution))))
                # y_pixel = int(round(mt.floor((self.particles[i, 1] - self.map_origin[1]) / (10*self.resolution))))
                # for j in range(0, self.apNum):
                #     u = self.model[j*2][y_pixel,x_pixel]
                #     xigema = self.model[j*2+1][y_pixel,x_pixel]
                #     p *= mt.exp(-(u-observe[j])**2/(2*xigema**2))/xigema*10
                # pro = p
                # if pro==0:
                #     pro=0.01

                dis = (centerPredict[0] - self.particles[i, 0]) ** 2 + (centerPredict[1] - self.particles[
                    i, 1]) ** 2 + 0.01
                dis = dis ** 0.5
                pro = 1 / dis
            elif self.modelType == 'knn':
                #centerPredict = self.knn(level=observe, n=4)
                dis = (centerPredict[0] - self.particles[i, 0]) ** 2 + (centerPredict[1] - self.particles[
                    i, 1]) ** 2 + 0.01
                dis = dis ** 0.5
                pro = 1 / dis

            elif self.modelType == 'Nearest':
                for j in range(0, self.apNum):
                    if observe[j] != -100:
                        tempy = int(round(self.particles[i, 1] - self.origin[1]))
                        tempx = int(round(self.particles[i, 0] - self.origin[0]))
                        if tempx >= self.grid.shape[1]:
                            tempx = self.grid.shape[1] - 1
                        elif tempx < 0:
                            tempx = 0
                        if tempy >= self.grid.shape[0]:
                            tempy = self.grid.shape[0] - 1
                        elif tempy < 0:
                            tempy = 0
                        predict = self.grid[tempy, tempx, j]
                        dis = dis + (predict - observe[j]) ** 2
                pro = mt.exp(-dis / 20.0 / 20.0 / 2)

            # dis=1.0/dis

            self.particles[i, 2] *= pro
            total = total + self.particles[i, 2]
        mean = [0, 0]
        for i in range(0, self.n):
            self.particles[i, 2] = self.particles[i, 2] / total
            mean += self.particles[i, :2] * self.particles[i, 2]
        return mean

    def ifResample(self, limit):
        liveDegree = 1. / sum(self.particles[:, 2] ** 2)
        if liveDegree <= limit:
            return 1
        else:
            return 0

    def particleResample(self):
        indices = []
        # 求出离散累积密度函数(CDF)
        C = [0.] + [sum(self.particles[:i + 1, 2]) for i in range(self.n)]
        # 选定一个随机初始点
        u0, j = rand.random(), 0
        for u in [(u0 + i) / self.n for i in range(self.n)]:  # u 线性增长到 1
            while u > C[j]:  # 碰到小粒子，跳过
                j += 1
            indices.append(j - 1)  # 碰到大粒子，添加，u 增大，还有第二次被添加的可能
        self.particles = self.particles[indices, :]  # 返回大粒子的下标
        self.particles[:, 2] = 1.00 / self.n
        # self.particleAbandon()
        return indices

    def particleAbandon(self):
        total = 0

        width, length = self.map.shape
        for i in range(0, self.n):
            x_pixel = int(mt.floor((self.particles[i, 0] - self.map_origin[0]) / self.resolution))
            y_pixel = int(mt.floor((self.particles[i, 1] - self.map_origin[1]) / self.resolution))
            if x_pixel < 0 or x_pixel >= length or y_pixel < 0 or y_pixel >= width:
                self.particles[i, 2] *= 0.01
            else:
                # becareful about the x,y in array
                if self.map[y_pixel, x_pixel] < 225:
                    self.particles[i, 2] *= 0.01
                    # print(self.particles[i, 0],",",self.particles[i, 1],"in wall")

            total += self.particles[i, 2]
        self.particles[:, 2] = self.particles[:, 2] / total

        return 0

    def getMean(self):
        mean = [0, 0, 0]
        for i in range(self.n):
            mean[:2] += self.particles[i, :2] * self.particles[i, 2]
            mean[2] += self.particles[i, 3] * self.particles[i, 2]
        return np.array(mean)
