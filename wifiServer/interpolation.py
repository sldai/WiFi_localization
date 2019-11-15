#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@author: daishilong
@contact: daishilong1236@gmail.com

'''

import numpy as np
from scipy import interpolate
import pylab as pl
import matplotlib as mpl
import scipy.io as scio
data = np.loadtxt("E:/WiFi/实验室6楼/wifiData/2018-05-13 22_05_01.txt", dtype=float, delimiter=',')
def func(x, y):
    return (x + y) * np.exp(-5.0 * (x ** 2 + y ** 2))
grid = scio.loadmat("6b"+"/grid/" + 'grid.mat')
grid = grid['grid']
row = grid.shape[0]
col = grid.shape[1]
origin = scio.loadmat("6b"+"/grid/" +  'origin.mat')
origin = origin['origin'][0]

# X-Y轴分为15*15的网格
y, x = np.mgrid[0:row, 0:col]

fvals = grid[:,:,0]  # 计算每个网格点上的函数值  15*15的值

# 三次样条二维插值
newfunc = interpolate.interp2d(x, y, fvals, kind='linear')

# 计算100*100的网格上的插值
xnew = np.linspace(0, col, 2*col)  # x
ynew = np.linspace(0, row, 2*row)  # y
fnew = newfunc(xnew, ynew)  # 仅仅是y值   100*100的值

# 绘图
# 为了更明显地比较插值前后的区别，使用关键字参数interpolation='nearest'
# 关闭imshow()内置的插值运算。
pl.subplot(121)
im1 = pl.imshow(fvals, extent=[0, col, 0, row], cmap=mpl.cm.hot, interpolation='nearest', origin="lower")  # pl.cm.jet
# extent=[-1,1,-1,1]为x,y范围  favals为
pl.colorbar(im1)

pl.subplot(122)
im2 = pl.imshow(fnew, extent=[0, col, 0, row], cmap=mpl.cm.hot, interpolation='nearest', origin="lower")
pl.colorbar(im2)

pl.show()