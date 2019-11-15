#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import numpy as np
import matplotlib.pyplot as plt

particle_or_not = "particle_fusion"
# particle_or_not = "pure_wifi"
# knn
plt.rcParams["font.size"] = 12
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
err_plot = []
err_sojourn_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/sojourn_knn.csv", dtype=float, delimiter=',')
err_sojourn_list = np.linalg.norm(err_sojourn_list,axis=1, keepdims=True)
err_survey0_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/survey0_knn.csv", dtype=float, delimiter=',')
err_survey0_list = np.linalg.norm(err_survey0_list,axis=1, keepdims=True)
err_survey1_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/survey1_knn.csv", dtype=float, delimiter=',')
err_survey1_list = np.linalg.norm(err_survey1_list,axis=1, keepdims=True)
err_recover0_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/recover0_knn.csv", dtype=float, delimiter=',')
err_recover0_list = np.linalg.norm(err_recover0_list,axis=1, keepdims=True)
err_recover1_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/recover1_knn.csv", dtype=float, delimiter=',')
err_recover1_list = np.linalg.norm(err_recover1_list,axis=1, keepdims=True)
plt.figure()
# plt.hist(abs(np.array(err_sojourn_list)),50, normed=1, histtype='step', color='r', alpha=1, cumulative=True, rwidth=0.8, label="baseline")
plt.hist(abs(np.array(err_survey0_list)),50, normed=1, histtype='step', color='g', alpha=1, cumulative=True, rwidth=0.8, label="Raw KNN")
plt.hist(abs(np.array(err_survey1_list)),50, normed=1, histtype='step', color='b', alpha=1, cumulative=True, rwidth=0.8, label="Resurvey kNN")
# plt.hist(abs(np.array(err_recover0_list)),50, normed=1, histtype='step', color='m', alpha=1, cumulative=True, rwidth=0.8, label="recover")
# plt.hist(abs(np.array(err_recover1_list)),50, normed=1, histtype='step', color='c', alpha=1, cumulative=True, rwidth=0.8, label="both")
# plt.legend()
# bayes
err_sojourn_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/sojourn_bayes.csv", dtype=float, delimiter=',')
err_sojourn_list = np.linalg.norm(err_sojourn_list,axis=1, keepdims=True)
err_survey0_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/survey0_bayes.csv", dtype=float, delimiter=',')
err_survey0_list = np.linalg.norm(err_survey0_list,axis=1, keepdims=True)
err_survey1_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/survey1_bayes.csv", dtype=float, delimiter=',')
err_survey1_list = np.linalg.norm(err_survey1_list,axis=1, keepdims=True)
err_recover0_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/recover0_bayes.csv", dtype=float, delimiter=',')
err_recover0_list = np.linalg.norm(err_recover0_list,axis=1, keepdims=True)
err_recover1_list = np.loadtxt("survey_results/local_result/"+particle_or_not+"/recover1_bayes.csv", dtype=float, delimiter=',')
err_recover1_list = np.linalg.norm(err_recover1_list,axis=1, keepdims=True)
# plt.figure()
# plt.hist(abs(np.array(err_sojourn_list)),50, normed=1, histtype='step', color='r', alpha=1, cumulative=True, rwidth=0.8, label="baseline")
plt.hist(abs(np.array(err_survey0_list)),50, normed=1, histtype='step', color='orange', alpha=1, cumulative=True, rwidth=0.8, label="Raw Bayes")
plt.hist(abs(np.array(err_survey1_list)),50, normed=1, histtype='step', color='r', alpha=1, cumulative=True, rwidth=0.8, label="Resurvey Bayes")
# plt.hist(abs(np.array(err_recover0_list)),50, normed=1, histtype='step', color='m', alpha=1, cumulative=True, rwidth=0.8, label="recover")
# plt.hist(abs(np.array(err_recover1_list)),50, normed=1, histtype='step', color='c', alpha=1, cumulative=True, rwidth=0.8, label="both")
plt.xlim([0, 10])
plt.legend()
plt.xlabel("Localization Error (m)")
plt.ylabel("CDF")
plt.tick_params
plt.tight_layout()
plt.show()