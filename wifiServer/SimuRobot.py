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

modelPath="./model/svm/"
gridPath="./grid/"
data=np.loadtxt("E:/WiFi/实验室6楼/wifiData/行人验证/lastpdr.csv", dtype=float, delimiter=',')
#wall=np.loadtxt("C:/Users/lenovo/Desktop/wall.txt", dtype=float, delimiter=',')
apNum=20
trainingData=data[291:]
trainingData=np.vstack((data[:99], trainingData))
testingData=data[:]
length=len(testingData)
y=[]
model=[]

X = trainingData[:,:2]
grid=scio.loadmat(gridPath+'gridignore.mat')
origin=scio.loadmat(gridPath+'origin.mat')
grid=grid['grid']
origin=origin['origin'][0]



for i in range(0,apNum):
    temp=joblib.load(modelPath+"ap"+str(i)+".pkl")#载入学习模型
    model.append(temp)


#particleFilter
def knn(grid,level,apNum,n):
    nnlist=[]
    row=grid.shape[0]
    col=grid.shape[1]
    for i in range(row):
        for j in range(col):
            if grid[i,j,0]!=0:
                dis=0
                for num in range(apNum):
                    if level[num]!=-100:
                        dis+=(level[num]-grid[i][j][num])**2
                dis=1.0/(dis**0.5+0.01)
                nnlist.append([j,i,dis])
    nnlist=np.array(nnlist)
    mean=[origin[0],origin[1]]
    nnlist = nnlist[np.lexsort(-nnlist.T)]
    nnlist=nnlist[:n]
    nnlist[:,2]=nnlist[:,2]/sum(nnlist[:,2])
    for i in range(n):
        mean+=nnlist[i,:2]*nnlist[i,2]
    return mean
dis=[]
for i in range(len(testingData)):
    mean=knn(grid,testingData[i,2:],14,8)
    xy=testingData[i,:2]
    #dis+=abs(xy-mean)
    dis.append(xy-mean)
dis=np.array(dis)

def particleInitial(beginPoint,n):
    particles=[]
    for i in range(0,n):
        particles.append([beginPoint[0]+rand.uniform(-3,3), beginPoint[1]+rand.uniform(-0.2,0.2),1.0/n])
    particles=np.array(particles)
    return particles
def particleMove(particles,n,move):
    for i in range(0, n):
        particles[i,:2]+=move+[rand.uniform(0.5,-0.5),rand.uniform(0.5,-0.5)]
        if particles[i,1]>1:
            particles[i,1]=1
    return 0
def particleUpdate(particles,n,observe):
    total = 0
    for i in range(0, n ):
        dis=0

        for j in range(0, 14):
            if observe[j]!=-100:
                temp_clf = model[j]
                predict = temp_clf.predict([particles[i, :2]])
                dis = dis + (predict - observe[j]) * (predict - observe[j])

        #dis=1.0/dis
        dis=mt.exp(-dis/10.0/10.0/2)
        particles[i,2]*=dis
        total = total + particles[i,2]
    mean=[0,0]
    for i in range(0,n):
        particles[i,2]=particles[i,2]/total
        mean+=particles[i,:2]*particles[i,2]
    return mean

def ifResample(particles,limit):
    liveDegree=1./sum(particles[:,2]**2)
    if liveDegree<=limit:
        return 1
    else:
        return 0

def particleResample(particles,n):
    indices = []
    # 求出离散累积密度函数(CDF)
    C = [0.] + [sum(particles[:i + 1,2]) for i in range(n)]
    # 选定一个随机初始点
    u0, j = rand.random(), 0
    for u in [(u0 + i) / n for i in range(n)]:  # u 线性增长到 1
        while u > C[j]:  # 碰到小粒子，跳过
            j += 1
        indices.append(j - 1)  # 碰到大粒子，添加，u 增大，还有第二次被添加的可能
    return indices

def particleRadUpdate(particles,n,observe):
    total = 0
    for i in range(0, n ):
        dis=0

        for j in range(0, 14):
            temp_clf=model[j]
            predict=temp_clf.predict([particles[i,:2]])
            dis=dis+(predict-observe[j])*(predict-observe[j])
        #dis=1.0/dis
        dis=mt.exp(-dis/10.0/10.0/2)
        particles[i,2]*=dis
        total = total + particles[i,2]
    mean=[0,0]
    for i in range(0,n):
        particles[i,2]=particles[i,2]/total
        mean+=particles[i,:2]*particles[i,2]
    return mean
def particleAbandon(particles,n,wall):
    total=0
    for i in range(0,n):
        if wall[int(round(particles[i,0]+60)),int(round(particles[i,1]+10))]==0:
            particles[i,2]=0

        total+=particles[i,2]
    particles[:,2]=particles[:,2]/total
    return 0

print("move:")
#beginPoint=knn(grid,testingData[0,2:],apNum,8)
#particles=particleInitial(beginPoint,100)
pF=particleFilter(apNum,'GP','./6b')
ini=pF.knn(testingData[0,4:(4+apNum)],4)
pF.particleInitial(ini,100)
mean=[]
PFerr=[]
KnnErr=[]
plt.figure()

#plt.ion()
angle0=209
#particleResult=open("C:/Users/lenovo/Desktop/particleResult.txt",'w')
for i in range(0+1,length):
    #move = testingData[i, :2] - testingData[i-1, :2]+[rand.uniform(0.1,-0.1),rand.uniform(-0.1,0.1)]
    #observe = testingData[i, 2:(2 + apNum)]
    #pF.particleMove(move)  # 利用类
    #pF.particleUpdate(observe)
    if testingData[i,1]==1:
        move = [testingData[i,4]*mt.cos(mt.radians(-testingData[i,5]+209)),testingData[i,4]*mt.sin(mt.radians(-testingData[i,5]+209))]
        pF.particleMove(np.array(move))
    elif testingData[i,1]==2:
        observe=testingData[i,4:(4+apNum)]
        pF.particleUpdate(observe)
        pp=pF.knn(observe,11)
    elif testingData[i,1]==0:
        continue


    # particleMove(particles, 100, move)不利用类
    #
    # particleAbandon(particles,100,wall)
    # particleUpdate(particles,100,observe)
    # if ifResample(particles,50)==1:
    #     particles = particles[particleResample(particles,100), :]  # 返回大粒子的下标
    #     particles[:, 2] = 1.0 / 100
    #     particleAbandon(particles, 100, wall)
    #     print("*********")
    # tempmean =[0,0]
    # for num in range(0,100):
    #     tempmean+=particles[num,:2]*particles[num,2]


    if pF.ifResample(50)==1:
        pF.particleResample()
    tempmeancopy=pF.getMean()[:2]




    #tempmeancopy=pF.knn(observe,11)利用knn

    mean.append(tempmeancopy)
    #print(testingData[i, :2] - tempmeancopy)
    # particleResult.write(str(np.linalg.norm(testingData[i, :2] - tempmean))+"\n")
    plt.clf()
    #plt.axis([pF.origin[0] - 5, 60, pF.origin[1] - 5, 20])
    plt.axis([pF.origin[0]-5, 100, pF.origin[1]-10, 100])
    plt.plot(pF.particles[:, 0], pF.particles[:, 1], 'ro')
    #plt.plot(tempmeancopy[0], tempmeancopy[1], 'ro')
    if testingData[i, 1] == 1:
        plt.plot(testingData[i, 2], testingData[i, 3], 'go')
        real=[testingData[i, 2], testingData[i, 3]]

    else:
        plt.plot(testingData[i, 2], testingData[i, 3], 'go')
        real = [testingData[i, 2], testingData[i, 3]]
        plt.plot(pp[0], pp[1], 'bo')
        PFerr.append((real[:] - tempmeancopy[:]))
        KnnErr.append((real[:] - pp[:]))


    print(i,':',real[:]-tempmeancopy[:])
    #plt.plot(testingData[i,0],testingData[i,1],'go')
    plt.pause(0.00001)

#particleResult.close()
plt.figure()

mean=np.array(mean)
plt.plot(mean[:,0],mean[:,1],'r')
plt.plot(testingData[:,2],testingData[:,3],'g')
#plt.axis([pF.origin[0]-5, 60, pF.origin[1]-5, 20])
plt.axis([pF.origin[0]-5, 100, pF.origin[1]-5, 100])
#plt.legend(['result','actual'])
PFerr=np.array(PFerr)
KnnErr=np.array(KnnErr)
np.savetxt("PfSvmErr.csv",PFerr,fmt='%f',delimiter=',',newline='\r\n')
np.savetxt("2restoreSemi.csv",KnnErr,fmt='%f',delimiter=',',newline='\r\n')
plt.show()