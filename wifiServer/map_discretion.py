#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''

import numpy as np
from numpy import linalg
import math
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as patches
class mapDiscretion:
    def __init__(self, map_input):
        self.group_list = []
        self.map_array = np.array(map_input)
        (self.height, self.width) = map_input.shape
        self.group_num = 0
        self.group_ref_loc_list = []
        self.interval = 15
        self.group_angle_list = []

    def get_group_list(self):
        self.group_num = np.max(self.map_array)

        for i in range(self.group_num):
            self.group_list.append([])

        for x in range(self.height):
            for y in range(self.width):
                pixel_value = self.map_array[x, y]
                if pixel_value>0:
                    self.group_list[pixel_value-1].append(np.array([x, y]))

    def get_angle(self, group):
        covariances = np.cov(np.array(group).transpose())
        v, w = linalg.eigh(covariances)
        index = 0 if v[0]>v[1] else 1
        u = w[index] / linalg.norm(w[index])
        angle = np.arctan(u[1] / u[0])
        return angle

    def rotation(self, theta, P, type):
        R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        if type == 0:
            return np.matmul(R, P)
        else:
            return np.matmul(np.transpose(R), P)


    def find_minimun_rectangle(self, group, theta):

        group_rotated = [self.rotation(theta, np.array(pixel), 1) for pixel in group]
        group_rotated = np.array(group_rotated)
        x_min = min(group_rotated[:,0])
        x_max = max(group_rotated[:,0])
        y_min = min(group_rotated[:,1])
        y_max = max(group_rotated[:,1])
        return x_min, x_max, y_min, y_max

    def discretize_one_group(self, group):
        group_value = self.map_array[group[0][0], group[0][1]]
        theta = self.get_angle(group)
        x_min, x_max, y_min, y_max = self.find_minimun_rectangle(group, theta)
        left_bot = self.rotation(theta, np.array([x_min, y_min]), 0)
        right_bot = self.rotation(theta, np.array([x_max, y_min]), 0)
        right_top = self.rotation(theta, np.array([x_max, y_max]), 0)
        left_top = self.rotation(theta, np.array([x_min, y_max]), 0)
        # plt.plot([left_bot[1], right_bot[1]], [left_bot[0], right_bot[0]], color = 'black')
        # plt.plot([right_bot[1], right_top[1]], [right_bot[0], right_top[0]], color = 'black')
        # plt.plot([right_top[1], left_top[1]], [right_top[0], left_top[0]], color = 'black')
        # plt.plot([left_top[1], left_bot[1]], [left_top[0], left_bot[0]], color = 'black')
        ref_loc_list = []
        for y_new in np.arange(y_min+4, y_max, self.interval):
            for x_new in np.arange(x_min, x_max, self.interval):

                coord_world = self.rotation(0, np.array([x_new, y_new]), 0)
                coord_world_check=np.array([int(round(coord_world[0])),int(round(coord_world[1]))], dtype=np.int)

                check_inside_map = (coord_world_check[0] >= 0) \
                                   & (coord_world_check[1] >= 0) \
                                   & (coord_world_check[0] < self.height) \
                                   & (coord_world_check[1] < self.width)
                if check_inside_map:
                    check_inside_group = self.map_array[coord_world_check[0], coord_world_check[1]] \
                                         == group_value
                    if check_inside_group:
                        ref_loc_list.append(coord_world)

        return ref_loc_list, theta

    def discretize_no_rot(self):
        top = np.max(np.array(self.group_list[0])[:,0])
        bot = np.min(np.array(self.group_list[0])[:,0])
        left = np.min(np.array(self.group_list[0])[:,1])
        right = np.max(np.array(self.group_list[0])[:,1])
        plt.gca().add_patch(patches.Rectangle((left, bot), right-left, top-bot, linewidth=2, edgecolor='black', facecolor='none'))
        bot = np.min(np.array(self.group_list[0])[:, 0]) + 5
        left = np.min(np.array(self.group_list[0])[:, 1]) + 5
        ref_loc_list = []
        a = left
        b = right
        for y_new in np.arange(bot, top, self.interval):
            for x_new in np.arange(a, b, int((b-a)/abs((b-a)))*self.interval):
                if self.map_array[y_new, x_new] != 0:
                    ref_loc_list.append(np.array([x_new, y_new]))
            tmp = a
            a = b
            b = tmp
        ref_loc_list = np.array(ref_loc_list)
        plt.plot(ref_loc_list[:, 0], ref_loc_list[:, 1], 'r.', ms=10)
        return ref_loc_list

    def discretize_all(self):
        for group in self.group_list:
            ref_loc_list, angle = self.discretize_one_group(group)
            self.group_angle_list.append(angle)
            if len(ref_loc_list)>0:
                self.group_ref_loc_list.append(ref_loc_list)
                ref_loc_list = np.array(ref_loc_list)



                plt.plot(ref_loc_list[:,1], ref_loc_list[:,0], 'r.', ms=10)

    def line_path_one_group(self, ref_loc_list, theta):
        ref_loc_list_tmp = np.array(ref_loc_list)
        for point_index in range(1,len(ref_loc_list_tmp)):
            point1 = ref_loc_list_tmp[point_index-1]
            point2 = ref_loc_list_tmp[point_index]
            angle = math.atan((point2[1]-point1[1]) / (point2[0]-point1[0]))
            line_length = linalg.norm(point2-point1)
            if abs(angle-theta)<0.1 and abs(line_length-self.interval)<=1:
                plt.plot(ref_loc_list_tmp[point_index-1:point_index+1, 1], ref_loc_list_tmp[point_index-1:point_index+1, 0], linewidth = 2, linestyle = '-',color = 'm')

    def line_path_groups(self):
        for i in range(self.group_num):
            theta = self.group_angle_list[i]
            ref_loc_list = self.group_ref_loc_list[i]
            self.line_path_one_group(ref_loc_list, theta)

    # def plot_results(self):
    #     for group in self.group_list:
    #         group_array = np.array(group)
    #         plt.scatter(group_array[:, 1] , group_array[:, 0], color=)
def colormap():
    # 白青绿黄红
    cdict = ['#FFFFFF', 'c', 'cornflowerblue', 'gold',
                              'darkorange']
    # 按照上面定义的colordict，将数据分成对应的部分，indexed：代表顺序
    return colors.ListedColormap(cdict, 'indexed')

import itertools

color_iter = ['navy', 'c', 'cornflowerblue', 'gold',
                              'darkorange']
def plot_map(map_data):
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            plt.scatter(i, j, color = color_iter[map_data[i,j]-1])

def plot_without_border(img, cmap):
    fig = plt.figure(figsize=(4.5,3))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(img, cmap=cmap)

def draw_arrow_about_path():
    # plt.annotate("", xy=(13, 18), xytext=(13, 137), arrowprops=dict(arrowstyle="->"))
    # # plt.annotate("", xy=(13, 18), xytext=(13, 137), arrowprops=dict(arrowstyle="->"))
    #
    # plt.annotate("", xy=(101, 150), xytext=(13, 150), arrowprops=dict(arrowstyle="->"))
    # plt.annotate("", xy=(13, 160), xytext=(101, 160), arrowprops=dict(arrowstyle="->"))
    #
    plt.annotate("", xy=(250, 137), xytext=(136, 137), arrowprops=dict(arrowstyle="->"))
    plt.annotate("", xy=(136, 156), xytext=(250, 156), arrowprops=dict(arrowstyle="->"))

    # plt.annotate("", xy=(38, 34), xytext=(83, 34), arrowprops=dict(arrowstyle="->"))
    # plt.annotate("", xy=(83, 50), xytext=(38, 50), arrowprops=dict(arrowstyle="->"))



if __name__ == '__main__':

    map_data = np.load('map_data/merge_similar.npy')
    my_cmap = colormap()

    plot_without_border(map_data, my_cmap)
    # draw_arrow_about_path()

    plot_without_border(map_data, my_cmap)

    map_discret = mapDiscretion(map_data)
    map_discret.get_group_list()
    ref_loc_list = map_discret.discretize_no_rot()
    for index in range(len(ref_loc_list)-1):
        plt.annotate("", xy=(ref_loc_list[index+1, 0], ref_loc_list[index+1, 1]), xytext=(ref_loc_list[index, 0], ref_loc_list[index, 1]), arrowprops=dict(arrowstyle="->",lw=2))


    # map_discret.line_path_groups()
    plt.axis('off')
    plt.show()