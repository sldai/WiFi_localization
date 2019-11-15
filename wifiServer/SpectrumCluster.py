#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
# coding=gbk
import numpy as np
import time
from sklearn.cluster import SpectralClustering
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabaz_score

# 生成500个 6 维的数据集， 分为 5 个簇
X, y = make_blobs(n_samples=500, n_features=6, centers=5, cluster_std=[0.4, 0.4, 0.3, 0.3, 0.4],
                  random_state=666)
print(X.shape)
print(y.shape)
model = SpectralClustering()
y_pre = model.fit_predict(X)
score = calinski_harabaz_score(X, y_pre)
print('calinski_harabaz_score:' + str(score))  # calinski_harabaz_score:11509.943254338412


# 使用高斯核，对n_cluster 和 gamma 进行调参
start = time.clock()
best_score, best_k, best_gamma = 0, 0, 0
for gamma in (0.01, 0.1, 1, 5):
    for k in (3, 4, 5, 6):
        y_pre = SpectralClustering(n_clusters=k, gamma=gamma).fit_predict(X)
        score = calinski_harabaz_score(X, y_pre)
        print('calinski_harabaz_score: %.3f, k value: % d, gamma value: %f' % (calinski_harabaz_score(X, y_pre),
                                                                               k, gamma))
        if score > best_score:
            best_score = score
            best_k = k
            best_gamma = gamma

print('best_score:%.3f, best_k: %d , best_gamma: %.3f' % (best_score, best_k, best_gamma))

end = time.clock()
real_time = end - start
print('spending time: %.3f ' % real_time + 's')
