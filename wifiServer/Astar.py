# -*- coding: utf-8 -*-

import numpy as np
from heapq import heappush, heappop
import scipy.io as scio
from multiprocessing import Pool
from functools import partial
def heuristic_cost_estimate(neighbor, goal):
    x = neighbor[0] - goal[0]
    y = neighbor[1] - goal[1]
    return abs(x) + abs(y)


def dist_between(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path


# astar function returns a list of points (shortest path)
def astar(array, start, goal):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # 8个方向

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic_cost_estimate(start, goal)}

    openSet = []
    heappush(openSet, (fscore[start], start))  # 往堆中插入一条新的值

    # while openSet is not empty
    while openSet:
        # current := the node in openSet having the lowest fScore value
        current = heappop(openSet)[1]  # 从堆中弹出fscore最小的节点

        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j in directions:  # 对当前节点的 8 个相邻节点一一进行检查
            neighbor = current[0] + i, current[1] + j

            ## 判断节点是否在地图范围内，并判断是否为障碍物
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] < 204:  # 0为障碍物
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            # Ignore the neighbor which is already evaluated.
            if neighbor in close_set:
                continue

            # The distance from start to a neighbor via current
            tentative_gScore = gscore[current] + dist_between(current, neighbor)

            if neighbor not in [i[1] for i in openSet]:  # Discover a new node
                heappush(openSet, (fscore.get(neighbor, np.inf), neighbor))
            elif tentative_gScore >= gscore.get(neighbor, np.inf):  # This is not a better path.
                continue

                # This path is the best until now. Record it!
            came_from[neighbor] = current
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tentative_gScore + heuristic_cost_estimate(neighbor, goal)

    return False

from PIL import Image
import matplotlib.pyplot as plt

glist=np.loadtxt("list.txt", dtype=float, delimiter=' ')
img = Image.open('E:/project/PycharmProjects/wifiServer/6b/map/mymap1cost.bmp')
map = np.array(img)  # 图像转化为二维数组
map = map[::-1]
scale = 10
mat= np.zeros([len(glist),len(glist)])

def astarList(index_list):
    i=index_list[0]
    j=index_list[1]
    # s_x = int(round(glist[i, 2] / scale))
    # s_y = int(round(glist[i, 3] / scale))
    # g_x = int(round(glist[j, 2] / scale))
    # g_y = int(round(glist[j, 3] / scale))
    dist = np.linalg.norm(glist[i, :2]-glist[j, :2])
    if dist<=0.7*8:
        cost = sum(abs(glist[i, :2]-glist[j, :2]))
    else:
        cost = 10000
    mat[i,j]=cost
    mat[j,i]=cost

if __name__ == "__main__":


    input_list=[]
    for i in range(0,len(glist)-1):
        for j in range(i+1,len(glist)):
            input_list.append([i,j])
            #path = astar(map, (s_y, s_x), (g_y, g_x))
            # img = np.array(img.convert('RGB'))
            # img[s_y,s_x] = [0, 0, 255]
            # img[g_y, g_x] = [0, 0, 255]
            # plt.imshow(img)
            # plt.axis('off')
            # plt.show()
            #mat[i,j]=len(path)
            #print(str(i)+':'+str(len(path)))
        # 绘制路径
    # pool = Pool()
    # func = partial(astarList, mat)
    # pool.map(func, input_list)
    # pool.close()
    # pool.join()
    for l in range(len(input_list)):
        astarList(input_list[l])

    np.savetxt("jacantMat.csv", np.array(mat), fmt='%f', delimiter=',', newline='\r\n')
