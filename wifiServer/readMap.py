import yaml
import matplotlib.pyplot as plt
import numpy as np
import math as mt
import pylab as pl
import cv2
from mpl_toolkits.mplot3d import Axes3D
import os
def read_pgm(pgmf):
    """Return a raster of integers from a PGM as a list of lists."""
    p=pgmf.readline()
    width=int(pgmf.readline())
    height=int(pgmf.readline())
    #(width, height) = [int(i) for i in pgmf.readline().split()]
    depth = int(pgmf.readline())
    assert depth <= 255

    raster = []
    for y in range(height):
        row = []
        for y in range(width):
            row.append(ord(pgmf.read(1)))
        raster.append(row)
    return raster
def read_ros_mapall(map_yaml_path):
    temp = yaml.load(open(map_yaml_path))
    resolution = temp['resolution']
    map_origin = temp['origin']
    map_name = temp['image']

    mapData = read_ros_map(os.path.dirname(map_yaml_path) + '/' + map_name)
    map_cost = read_ros_map(os.path.dirname(map_yaml_path) + '/' + 'costmap.pgm')

    return mapData, map_origin, resolution,map_cost
def read_ros_map(map_path):

    map = open(map_path, 'rb')
    mapData = read_pgm(map)
    mapData = np.array(mapData)
    mapData = mapData[::-1]
    return mapData
'''
mapData=read_ros_map('./6b/map/mymap.pgm')
width,length=mapData.shape
for i in range(0,width,10):
    for j in range(0,length,10):
        if mapData[i,j]>230:
            plt.plot(j,i,'ro')
plt.show()
print(mapData[1050][100])
'''
def area(point,rectDefine):

    for i in range(len(rectDefine)):
        if point[0]<=rectDefine[i,2] and point[0]>rectDefine[i,0] and point[1]<=rectDefine[i,3] and point[1]>rectDefine[i,1]:
            return i

def world2picture(point, map_origin, resolution):
    x_pixel = int(round((point[0] - map_origin[0]) / resolution))
    y_pixel = int(round((point[1] - map_origin[1]) / resolution))
    return [y_pixel, x_pixel]
if __name__ == '__main__':

    f = open("./6b/map/mymap.yaml")
    temp = yaml.load(f)
    resolution = temp['resolution']
    map_origin = temp['origin']
    mapData, _, _ = read_ros_map('6b/map/mymap - cost.pgm')

    list = []
    interval = 0.7
    for k in range(1):
        direct = False
        area_list = []
        #if (rectOrder[k,2]-rectOrder[k,0])<(rectOrder[k,3]-rectOrder[k,1]):
        for x in np.arange(0, 50, interval):
            temp_list=[]
            direct = not direct
            for y in np.arange(-2, 75,interval):
                x_pixel = int(round((x - map_origin[0]) / resolution))
                y_pixel = int(round((y - map_origin[1]) / resolution))
                if mapData[y_pixel, x_pixel] > 225 :
                    temp_list.append([x, y])
            if direct==True:
                temp_list.reverse()
            area_list=area_list+temp_list
            # if len(temp_list) > 0:
            #     area_list.append(temp_list[0])
            #     area_list.append(temp_list[-1])
        #else:

        list=list+area_list
    # x=32.0
    # y=68.4
    x=3
    y=3
    x_pixel = int(round((x - map_origin[0]) / resolution))
    y_pixel = int(round((y - map_origin[1]) / resolution))
    list.insert(0, [x, y])
    list=np.array(list)
    np.savetxt("list.txt", np.array(list), fmt='%f', delimiter=' ', newline='\r\n')
    plt.plot(list[:, 0], list[:, 1], 'r.')
    plt.show()




    # gpr = np.loadtxt("csv/complete/meanRe.csv", dtype=float, delimiter=',')
    # std = np.loadtxt("csv/complete/stdRe.csv", dtype=float, delimiter=',')
    # wifiMap = np.ones([int(len(mapData)/10),int(len(mapData[0,:])/10)]) -1
    # # ax=[]
    # # sca = plt.figure().add_subplot(111, projection='3d')
    # # sca.scatter(std[:, 0], std[:, 1], std[:, 3], c='y')
    # # sca.set_zlabel('Z')
    # # sca.set_ylabel('Y')
    # # sca.set_xlabel('X')
    # for ap in range(20):
    #     meanMap = np.ones([int(len(mapData) / 10), int(len(mapData[0, :]) / 10)],int) - 1
    #     stdMap = np.ones([int(len(mapData) / 10), int(len(mapData[0, :]) / 10)],int) - 1
    #     for i in range(len(gpr)):
    #
    #         x = gpr[i, 0]
    #         y = gpr[i, 1]
    #         x_pixel = int(round(mt.floor((x - map_origin[0]) / interval)))
    #         y_pixel = int(round(mt.floor((y - map_origin[1]) / interval)))
    #         meanMap[y_pixel, x_pixel] = int(round(gpr[i, 2 + ap]+100))
    #         stdMap[y_pixel, x_pixel] = int(round(std[i, 2 + ap]))
    #     meanMap = meanMap[::-1]
    #     stdMap = stdMap[::-1]
    #
    #     #plt.imsave(wifiMap, cmap='gray')
    #     cv2.imwrite('model/GP/'+'ap'+str(ap)+'mean.jpg',meanMap)
    #     cv2.imwrite('model/GP/'+'ap'+str(ap) + 'std.jpg', stdMap)
    # plt.show()







