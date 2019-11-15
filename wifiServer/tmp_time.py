#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

from outlierInGP import DetectOutlier
import numpy as np
data = np.loadtxt("E:/project/PycharmProjects/wifiServer/survey_results/3F_square/resurveyed/survey0.csv", dtype=float, delimiter=',')[:,1:]
map_setting = {'ap_num': 19, 'interval': 0.8, 'origin': [0.0, 0.0], 'lost_signal': -100}
import time
process2 = DetectOutlier(data, map_setting, 1.8, [])
current_time = time.time()
process2.process()
print(time.time()-current_time)
