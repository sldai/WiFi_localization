#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import scipy.io as scio
import numpy as np
grid = scio.loadmat("0/" + 'grid.mat')
origin = scio.loadmat("0/" + 'origin.mat')

grid= grid['grid']
origin = origin['origin'][0]

interval = 1
h = grid.shape[0]
w = grid.shape[1]
meanCsv = []
for i in range(h):
    for j in range(w):
        if grid[i, j, 0] != 0:
            x = j*interval+origin[0]
            y = i*interval+origin[1]
            slot = np.hstack((np.array([x,y]),np.array(grid[i,j,:])))
            meanCsv.append(slot)
np.savetxt("0/mean.csv", np.array(meanCsv), fmt='%f', delimiter=',', newline='\r\n')

