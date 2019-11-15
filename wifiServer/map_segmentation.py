#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
from scipy import ndimage
from readMap import read_ros_mapall
import numpy as np
import cv2
from skimage import measure
import matplotlib.pyplot as pyplot
import math
from PIL import Image
from numpy import linalg
class mapSegmentation:
    def __init__(self, map_img, threshold):

        self.threshold = threshold
        self.map = map_img
        (self.rows, self.cols) = self.map.shape
        self.binary_image = np.array(self.map)
        self.dimage = np.array(self.map)
        self.free_list = []
        self.free_space_image = []

        self.group_list = []
        self.group_list_value = []
        self.group_list_size = []
        self.group_num = 0
        self.t_merging = 0.2
        self.m = 0.1
        self.contour_percentage = 0.3

    def get_binary_image(self):
        self.binary_image = np.array(self.map)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] > self.threshold:
                    self.binary_image[i][j] = 1
                    self.free_list.append([i,j])
                else:
                    self.binary_image[i][j] = 0
        # self.free_list = np.array(self.free_list)



    def get_distance_image(self):
        # get dimage
        self.dimage = ndimage.distance_transform_edt(self.binary_image)

    def get_free_space_image(self):
        self.get_binary_image()
        self.get_distance_image()

        # get fsi from dimage
        self.free_space_image = np.array(self.dimage)
        num=0
        for each_pixel in self.free_list:
            num+=1
            if num%10000==0:
                print(num)
            radius = self.dimage[each_pixel[0], each_pixel[1]]
            circle_list = self.circular_mask(each_pixel, int(np.floor(radius)))
            for pixel_in_circle in circle_list:
                # not obstacle
                if self.binary_image[pixel_in_circle[0], pixel_in_circle[1]] != 0:
                    if self.free_space_image[pixel_in_circle[0], pixel_in_circle[1]] <= radius:
                        self.free_space_image[pixel_in_circle[0], pixel_in_circle[1]] = radius

        np.save("map_data/fsi.npy", self.free_space_image)

    def circular_mask(self, center, radius):
        in_list = []
        left = max(center[1] - radius, 0)
        right = min(center[1] + radius, self.cols-1)
        bottom = min(center[0] + radius, self.rows-1)
        top = max(center[0] - radius, 0)
        for i in range(top,bottom+1):
            for j in range(left,right+1):
                if np.linalg.norm(np.array([i,j]) - center) <= radius:
                    in_list.append(np.array([i,j]))
        return in_list

    def region_group(self):
        free_list_tmp = self.free_list.copy()
        segmented_img = np.zeros([self.rows, self.cols], np.uint16)

        group_color = 1
        # iterate the free list to clear
        while len(free_list_tmp) != 0:
            seed = free_list_tmp.pop(0)
            self.group_list_value.append(self.free_space_image[seed[0], seed[1]])
            # find group of this seed
            one_group = self.region_growth(self.free_space_image, segmented_img, free_list_tmp, seed, group_color)
            self.group_list.append(one_group)
            group_color += 1

        self.group_num = group_color-1
        pyplot.figure()
        pyplot.imshow(segmented_img)
        np.save("map_data/region_group.npy", segmented_img)


    def region_growth(self, img, segmented_img, free_list, seed, color):
        # Parameters for region growing
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # points need iterating
        neighbor_points_list = []
        # points iterated, so we group these
        group_points_list = []
        group_value = img[seed[0], seed[1]]

        # Input image parameters
        height, width = img.shape

        # Initialize segmented output image

        segmented_img[seed[0], seed[1]] = color
        group_points_list.append(seed)


        # only iterate over can break this loop
        while True:
            # Loop through neighbor pixels
            for i in range(4):
                # Compute the neighbor pixel position
                x_new = seed[0] + neighbors[i][0]
                y_new = seed[1] + neighbors[i][1]

                # Boundary Condition - check if the coordinates are inside the image
                check_inside = (x_new >= 0) & (y_new >= 0) & (x_new < height) & (y_new < width)

                # Add neighbor if inside and not already in segmented_img
                if check_inside:

                    if img[x_new, y_new] == group_value:
                        if segmented_img[x_new, y_new] == 0:
                            neighbor_points_list.append([x_new, y_new])
                            segmented_img[x_new, y_new] = color


            if len(neighbor_points_list)!=0:
                # Update the seed value and delete it
                seed = neighbor_points_list.pop(0)
                group_points_list.append(seed)
                index = free_list.index(seed)
                free_list.pop(index)
            else:
                break
        return group_points_list

    def find_out_contour(self, group):
        # for each group, find the contour
        binary_map = np.zeros([self.rows, self.cols], dtype = np.uint8)
        for i in group:
            binary_map[i[0], i[1]] = 1

        # pyplot.figure()
        # pyplot.imshow(binary_map)

        # contours = measure.find_contours(binary_map, 0.8)
        # contours = np.array(np.round(contours[0]), dtype=np.uint8)

        _, contours, _ = cv2.findContours(binary_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        out_contours = []
        # Parameters for region growing
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for contour_one in contours:
            for contour_point in contour_one:
                inter_contour_point = contour_point[0]
                for i in range(4):
                    # Compute the neighbor pixel position
                    x_new = inter_contour_point[0] + neighbors[i][0]
                    y_new = inter_contour_point[1] + neighbors[i][1]
                    # Boundary Condition - check if the coordinates are inside the image
                    check_inside = (x_new >= 0) & (y_new >= 0) & (x_new < self.cols) & (y_new < self.rows)

                    # Add neighbor if inside and not already in segmented_img
                    if check_inside:
                        if binary_map[y_new, x_new] == 0:
                            out_contours.append([y_new, x_new])
                            binary_map[y_new, x_new] = 2

        return out_contours

    def check_belonging(self, point, group_list):
        for group_index in range(len(group_list)):
            if point in group_list[group_index]:
                return group_index
        # not free area
        return -1

    def merge_ripples(self):
        index_list = np.argsort(-np.array(self.group_list_value))
        self.group_list_value = [self.group_list_value[i] for i in index_list]
        self.group_list = [self.group_list[i] for i in index_list]

        group_list_value_tmp = self.group_list_value.copy()
        group_list_tmp = self.group_list.copy()

        # iterate all groups to merge ripples
        group_index = 0
        while True:
            group_num = len(group_list_tmp)
            contour_count = np.zeros([group_num])
            # find out contour
            out_contours = self.find_out_contour(group_list_tmp[group_index])
            for contour_point in out_contours:
                which_group = self.check_belonging(contour_point, group_list_tmp)
                if which_group != -1:
                    contour_count[which_group] += 1
            contour_count /= len(out_contours)
            # If more than 40% of the contour of a region is in contact
            # with a neighbor region, the region is merged in its neighbor.
            if np.any(contour_count >= self.contour_percentage):
                pixel_diff_list = np.abs(np.array(group_list_value_tmp) - group_list_value_tmp[group_index])
                pixel_diff_list = [pixel_diff_list[i] if contour_count[i] >= self.contour_percentage else np.inf for i in range(group_num)]
                min_index = pixel_diff_list.index(min(pixel_diff_list))
                group_list_tmp[min_index].extend(group_list_tmp[group_index])
                group_list_tmp.pop(group_index)
                group_list_value_tmp.pop(group_index)
                group_index = 0
            else:
                group_index += 1
                if group_index >= len(group_list_tmp):
                    break

        self.group_list = group_list_tmp
        self.group_list_value = group_list_value_tmp
        merged_map = np.array(self.binary_image)
        color = 1
        for one_group in group_list_tmp:
            for pixel in one_group:
                merged_map[pixel[0], pixel[1]] = color
            color += 1
        pyplot.figure()
        pyplot.imshow(merged_map)
        np.save("map_data/remove_ripples.npy", merged_map)

    def merge_neighbor_regions_with_similar_value(self):
        # consider from largest regions to smallest regions
        self.group_list_size = [len(group) for group in self.group_list]
        index_list = np.argsort(-np.array(self.group_list_size))
        self.group_list = [self.group_list[i] for i in index_list]
        self.group_list_size = [self.group_list_size[i] for i in index_list]
        self.group_list_value = [self.group_list_value[i] for i in index_list]

        group_list_size_tmp = self.group_list_size.copy()
        group_list_tmp = self.group_list.copy()
        group_list_value_tmp = self.group_list_value.copy()

        group_index = 0
        while True:
            group_num = len(group_list_tmp)
            contour_count = np.zeros([group_num])
            # find out contour
            out_contours = self.find_out_contour(group_list_tmp[group_index])
            for contour_point in out_contours:
                which_group = self.check_belonging(contour_point, group_list_tmp)
                if which_group != -1:
                    contour_count[which_group] += 1
            if np.any(contour_count >= 1):
                merge_done = False
                for neighbor_index in range(group_num):
                    if contour_count[neighbor_index] == 0:
                        continue

                    pV1 = group_list_value_tmp[group_index]
                    pV2 = group_list_value_tmp[neighbor_index]
                    check_similar = np.abs(pV1 - pV2) <= max(pV1, pV2) * (self.t_merging + self.m)
                    check_size = group_list_size_tmp[neighbor_index] <= 10
                    check = check_similar or check_size
                    if check:
                        group_list_tmp[group_index].extend(group_list_tmp[neighbor_index])
                        group_list_tmp.pop(neighbor_index)
                        group_list_value_tmp[group_index] = pV1
                        group_list_value_tmp.pop(neighbor_index)
                        group_list_size_tmp[group_index]+=group_list_size_tmp[neighbor_index]
                        group_list_size_tmp.pop(neighbor_index)
                        group_index = 0
                        merge_done = True
                        break
                if merge_done:
                    group_index = 0
                    continue

            # no merge
            group_index += 1
            if group_index >= len(group_list_tmp):
                break

        merged_map = np.array(self.binary_image)
        color = 1
        for one_group in group_list_tmp:
            for pixel in one_group:
                merged_map[pixel[0], pixel[1]] = color
            color += 1
        pyplot.figure()
        pyplot.imshow(merged_map)
        np.save("map_data/merge_similar.npy", merged_map)

    def rotation(self, theta, P, type):
        R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        if type == 0:
            return np.matmul(R, P)
        else:
            return np.matmul(np.transpose(R), P)

    def covariances2angle(self,covariances):
        v, w = linalg.eigh(covariances)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        angle = np.arctan(u[1] / u[0])
        return angle

    def get_covariances(self, group):
        return np.cov(np.array(group))

    def get_ref_point(self):
        for one_group in self.group_list:
            cov = self.get_covariances(one_group)
            theta = self.covariances2angle(cov)
            for i in range(len(one_group)):
                one_group[i] = self.rotation(theta, one_group[i], 1)


def detect_edge(img):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    height, width = img.shape
    edge_mask = np.ones([height,width])
    for x in range(height):
        for y in range(width):
            for i in range(len(neighbors)):
                x_new = x + neighbors[i][0]
                y_new = y + neighbors[i][1]
                # Boundary Condition - check if the coordinates are inside the image
                check_inside = (x_new >= 0) & (y_new >= 0) & (x_new < height) & (y_new < width)
                if check_inside:
                    if img[x,y] != img[x_new,y_new]:
                        edge_mask[x,y] = 0
                        break
    return edge_mask

def segment_map():
    map, origin, resolution, map_cost = read_ros_mapall(map_yaml_path='./6b/map/mymap.yaml')
    map_cost = map_cost[::-1]
    image=Image.fromarray(map_cost)
    image=image.resize((int(map_cost.shape[1]/3), int(map_cost.shape[0]/3)))
    image = np.array(image)
    threshold = 210
    map_seg = mapSegmentation(image, threshold)
    map_seg.get_free_space_image()
    fsi = map_seg.free_space_image
    pyplot.figure()
    pyplot.imshow(fsi)
    map_seg.region_group()
    map_seg.merge_ripples()
    map_seg.merge_neighbor_regions_with_similar_value()
    pyplot.show()

from matplotlib import colors

def colormap():
    # 白青绿黄红
    cdict = ['#FFFFFF', 'c', 'cornflowerblue', 'gold',
                              'darkorange']
    # 按照上面定义的colordict，将数据分成对应的部分，indexed：代表顺序
    return colors.ListedColormap(cdict, 'indexed')

def plot_edge():
    def plot_without_border(img, cmap):
        fig = pyplot.figure(figsize=(4.5,3))
        ax = pyplot.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(img, cmap=cmap)

    img = np.load("map_data/fsi.npy")
    plot_without_border(img, 'gray_r')

    img = np.load("map_data/region_group.npy")
    edge_map = detect_edge(img)
    plot_without_border(edge_map, cmap='gray')

    img = np.load("map_data/remove_ripples.npy")
    edge_map = detect_edge(img)
    plot_without_border(edge_map, cmap='gray')

    img = np.load("map_data/merge_similar.npy")
    plot_without_border(img,cmap=colormap())
    #
    # my_colormap = colormap()
    # pyplot.figure(figsize=(4.5,3))
    # pyplot.imshow(img, cmap=my_colormap)
    # pyplot.axis("off")



    pyplot.show()

if __name__ == '__main__':
    plot_edge()

