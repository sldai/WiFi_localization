# -- coding: utf-8 --
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
import math
class particleFilter:
    def __init__(self,apNum,modelType,Path):
        self.apNum=apNum
        self.model=[]
        self.modelType=modelType

        #load grid parameter
        grid = scio.loadmat(Path+"/grid/" + 'grid.mat')
        origin = scio.loadmat(Path+"/grid/" +  'origin.mat')
        self.grid = grid['grid']
        self.origin = origin['origin'][0]
        #load map
        f = open(Path+"/map/mymap.yaml")
        temp = yaml.load(f)
        self.resolution=temp['resolution']
        self.map_origin=temp['origin']
        map = temp['image']
        #map = open(Path+"/map/" + map, 'rb')
        self.map=read_ros_map(Path+"/map/" + map)
        #load machine learning
        if self.modelType=="svm":
            for i in range(0, self.apNum):
                temp = joblib.load(Path+"/model/svm/" + "ap" + str(i) + ".pkl")  # 载入学习模型
                self.model.append(temp)

        elif self.modelType=="knn":
            self.model=None
        elif self.modelType=='probability':
            self.model=None


    def read_ros_map(self,pgm_map):
        mapData = read_pgm(pgm_map)
        mapData = np.array(mapData)
        mapData = mapData[::-1]
        return mapData

    def knn(self, level,  n):
        nnlist = []
        row = self.grid.shape[0]
        col = self.grid.shape[1]
        for i in range(row):
            for j in range(col):
                if self.grid[i, j, 0] != 0:
                    dis = 0
                    for num in range(self.apNum):
                        if level[num] != -100:
                            dis += (level[num] - self.grid[i][j][num]) ** 2
                    pro = 1.0 / (dis ** 0.5 + 0.01)
                    nnlist.append([j, i, pro])
        nnlist = np.array(nnlist)
        mean = [self.origin[0], self.origin[1]]
        nnlist = nnlist[np.lexsort(-nnlist.T)]
        nnlist = nnlist[:n]
        nnlist[:, 2] = nnlist[:, 2] / sum(nnlist[:, 2])
        for i in range(n):
            mean += nnlist[i, :2] * nnlist[i, 2]
        return mean

    def particleInitial(self,beginPoint,num):
        particles = []
        self.n=num
        for i in range(0, self.n):
            particles.append([beginPoint[0] + rand.uniform(-3, 3), beginPoint[1] + rand.uniform(-3, 3), 1.0 / self.n, rand.uniform(0,2*math.pi)])
        self.particles = np.array(particles)
        return self.particles

    def particleMove(self, move):
        for i in range(0, self.n):
            self.particles[i, :2] += move + [rand.uniform(1, -1), rand.uniform(1, -1)]

        self.particleAbandon()
        return 0
        
    def particleMoveRobot(self, move):
        for i in range(0,self.n):
            self.particles[i, 0]+= move[0]*mt.cos(self.particles[i, 3]) - move[1]*mt.sin(self.particles[i, 3])+rand.uniform(-0.01, 0.01)
            self.particles[i, 1] += move[0] * mt.sin(self.particles[i, 3]) + move[1] * mt.cos(self.particles[i, 3])+rand.uniform(-0.01, 0.01)
            self.particles[i, 3] += move[2]+rand.uniform(-0.005, 0.005)
        self.particleAbandon()

    def particleUpdate(self,  observe):
        total = 0
        for i in range(0, self.n):
            dis = 0
            pro=1
            if self.modelType=='svm':
                for j in range(0, self.apNum):
                    if observe[j] != -100:
                        temp_clf = self.model[j]
                        predict = temp_clf.predict([self.particles[i, :2]])[0]
                        # if predict<-100:
                        #     predict = -80
                        
                        dis += (predict - observe[j]) **2
                        
                        #print(str(j)+','+str(dis))

                pro = mt.exp(-dis / 20.0 / 20.0 / 2)
            elif self.modelType=='dnn':


                for j in range(0, self.apNum):
                    if observe[j] != -100:
                        dis = dis + (self.model[j].predict([self.particles[i, :2]])[0,0] - observe[j]) **2
                pro = mt.exp(-dis / 20.0 / 20.0 / 2)
            elif self.modelType=='knn':
                centerPredict=self.knn(level=observe,n=1)
                dis=(centerPredict[0]-self.particles[i,0])**2+(centerPredict[1]-self.particles[i,1])**2+0.01
                dis=dis**0.5
                pro=1/dis



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
        #self.particleAbandon()
        return indices

    def particleAbandon(self):
        total = 0

        width,length=self.map.shape
        for i in range(0, self.n):
            x_pixel = int(mt.floor((self.particles[i, 0] - self.map_origin[0]) / self.resolution))
            y_pixel = int(mt.floor((self.particles[i, 1] - self.map_origin[1]) / self.resolution))
            if x_pixel<0 or x_pixel>=length or y_pixel<0 or y_pixel>=width:
                self.particles[i, 2] *= 0.01
            else:
                #becareful about the x,y in array
                if self.map[y_pixel,x_pixel] < 225:
                    self.particles[i, 2] *= 0.01
                    #print(self.particles[i, 0],",",self.particles[i, 1],"in wall")

            total += self.particles[i, 2]
        self.particles[:, 2] = self.particles[:, 2] / total

        return 0

    def getMean(self):
        mean=[0,0,0]
        for i in range(self.n):
            mean[:2]+=self.particles[i,:2]*self.particles[i,2]
            mean[2]+=self.particles[i,3]*self.particles[i,2]
        return mean
