#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
import numpy as np
from scipy.optimize import leastsq
import math
import matplotlib.pyplot as plt
dataWithout100=[]
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/Gaussin.csv", dtype=float, delimiter=',')

for i in range(len(data)):
    if data[i, 1]!=-100:
        dataWithout100.append([data[i,0], data[i,1]])
dataWithout100=np.array(dataWithout100)
X=dataWithout100[:,0]
Y=dataWithout100[:,1]
def func(p,x):
    k,b=p
    return 80/((2*math.pi)**0.5*b)*math.exp(-(x-k)**2 / (2*(b**2)))-100

def error(p,x,y):
    return func(p,x)-y #x、y都是列表，故返回值也是个列表

p0=np.array([-30, 20])
Para=leastsq(error,p0,args=(X,Y)) #把error函数中除了p以外的参数打包到args中

plt.plot()