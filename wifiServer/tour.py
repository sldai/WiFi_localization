from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
import matplotlib.pyplot as plt
import math as mt
from sklearn.cluster import KMeans
from Astar import astar
from readMap import read_ros_mapall,world2picture, read_ros_map
from sklearn import mixture
from scipy import linalg
import matplotlib as mpl

import itertools
import math

from sklearn.cluster import SpectralClustering

color_iter = itertools.cycle(['navy', 'c', 'cornflowerblue', 'gold',
                              'darkorange'])
# Distance callback
def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

  def distance_callback(from_node, to_node):
    return int(dist_matrix[from_node][to_node])

  return distance_callback
class Cover:
    def __init__(self, map_yaml_path, block_num, interval, start_point):
        self.map, self.origin, self.resolution, self.map_cost = read_ros_mapall(map_yaml_path=map_yaml_path)
        self.block_num = block_num
        self.refer_location = []
        self.interval = interval
        self.block_list = []
        self.block_center_list =[]
        self.block_angle_list = []
        self.final_list_static = []
        self.final_list_mobile = []
        self.white_area = []
        self.model = mixture.BayesianGaussianMixture(n_components=self.block_num,
                                                covariance_type='full')
        self.current_block_num = 0
        self.start_point =start_point
        self.threshold = 220
        self.size = np.array([self.map_cost.shape[1], self.map_cost.shape[0]])
    def dist_matrix_get(self, block, dist_type):
        dist_matrix = np.zeros([len(block),len(block)])
        if dist_type=='block':
            for i in range(0, len(block) - 1):
                for j in range(i + 1, len(block)):
                    dis = sum(abs(block[i] - block[j]))
                    dist_matrix[i,j]=dis
                    dist_matrix[j,i]=dis
        elif dist_type=='a*':
            for i in range(0, len(block) - 1):
                for j in range(i + 1, len(block)):
                    start = world2picture(block[i],self.origin, self.resolution)
                    goal = world2picture(block[j],self.origin, self.resolution)
                    dis = astar(self.map, (start[0], start[1]), (goal[0], goal[1]))
                    dist_matrix[i, j] = dis
                    dist_matrix[j, i] = dis
        elif dist_type=='eu':
            for i in range(0, len(block) - 1):
                for j in range(i + 1, len(block)):
                    dis = np.linalg.norm(block[i] - block[j])
                    dist_matrix[i,j]=dis
                    dist_matrix[j,i]=dis
        return dist_matrix
    def TSP(self, adjacentMat, best=0, time = 3):
        city_names = range(len(adjacentMat))
        # Distance matrix
        dist_matrix = adjacentMat

        tsp_size = len(city_names)
        num_routes = 1
        depot = 0

        # Create routing model
        if tsp_size > 0:
            routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
            search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
            if best ==1:
                search_parameters.local_search_metaheuristic = (
                    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
                search_parameters.time_limit_ms = time*1000
            # Create the distance callback.
            dist_callback = create_distance_callback(dist_matrix)
            routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
            # Solve the problem.
            assignment = routing.SolveWithParameters(search_parameters)
            if assignment:
                # Solution distance.
                print("Total distance: " + str(assignment.ObjectiveValue()) + " miles\n")
                # Display the solution.
                # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
                route_number = 0
                index = routing.Start(route_number)  # Index of the variable for the starting node.
                route = ''
                routeList = []
                while not routing.IsEnd(index):
                    # Convert variable indices to node indices in the displayed route.
                    routeList.append(routing.IndexToNode(index))
                    route += str(city_names[routing.IndexToNode(index)]) + ' -> '
                    index = assignment.Value(routing.NextVar(index))

                routeList.append(routing.IndexToNode(index))
                route += str(city_names[routing.IndexToNode(index)])
                #routeList = np.array(routeList)
                # np.savetxt("ruote.csv", np.array(routeList), fmt='%f', delimiter=',', newline='\r\n')
                print("Route:\n\n" + route)
                return routeList
            else:
                print('No solution found.')
        else:
            print('Specify an instance greater than 0.')

    def divide_combine(self):


        current_block_num = len(self.block_list)
        incision = []
        if current_block_num==0:
            print('no block')
            return
        else:
            self.final_list_static+=self.block_list[0]
        for i in range(current_block_num-1):
            index1,index2 = self.find_closest_point(self.block_list[i], self.block_list[i+1])
            self.right_shift(self.block_list[i+1], index2)
            incision.append(index1+1)

        for i in range(current_block_num-1):
            self.final_list_static[incision[i]:incision[i]]=self.block_list[i+1]
            if i!=current_block_num-1-1:
                incision[i + 1] += incision[i]
        self.final_list_static=np.array(self.final_list_static)
        return

    def right_shift(self, lt, index):
        right = lt[:index]
        left = lt[index:]
        lt.clear()
        lt.extend(left)
        lt.extend(right)

    def find_closest_point(self,block1, block2):
        index1=0
        index2=0
        short_path = 100
        for i in range(len(block1)):
            for j in range(len(block2)):
                temp_path = np.linalg.norm(block1[i]-block2[j])
                if short_path>temp_path:
                    short_path=temp_path
                    index1 = i
                    index2 = j
        return index1,index2


    def cluster_block(self, type=0):
        self.get_all_grid()
        X = np.array(self.white_area)
        self.model.fit(X)
        label = self.model.predict(X)

        self.plot_results(X, label, self.model.means_, self.model.covariances_, 1,
                     'Bayesian Gaussian Mixture with a Dirichlet process prior')
        for i in range(self.block_num):
            if len(X[label[:]==i])>0:
                # self.block_list.append(X[label[:]==i])
                self.block_center_list.append(self.model.means_[i])
                temp_angle = self.covariances2angle(self.model.covariances_[i])
                temp_block = X[label[:]==i,:]
                self.block_angle_list.append(temp_angle)
                if type == 0:
                    self.block_list.append(self.get_list_from_block(temp_angle, temp_block, i))
                else:
                    self.block_list.append(self.get_line_from_block(temp_angle, temp_block, i))
        self.current_block_num = len(self.block_center_list)
    def get_list_from_block(self, angle, block, label):
        for i in range(len(block)):
            block[i] = self.rotation(angle, block[i], 1)
        x_min = min(block[:,0])
        x_max = max(block[:,0])
        y_min = min(block[:,1])
        y_max = max(block[:,1])
        temp_list =[]
        re = True
        for i in np.arange(x_min,x_max,self.interval):
            temp_temp_list = []
            re = not re
            for j in np.arange(y_min, y_max, self.interval):
                point_in_floor = self.rotation(angle, np.array([i, j]), 0)
                x_pixel, y_pixel = world2picture(point_in_floor,self.origin,self.resolution)
                if x_pixel>0 and x_pixel<self.size[0] and y_pixel<self.size[1] and y_pixel>0:
                    if self.map_cost[y_pixel, x_pixel]>self.threshold:
                        if self.model.predict([point_in_floor])[0] == label:
                            temp_temp_list.append(point_in_floor)
            if re:
                temp_temp_list.reverse()
            temp_list+=temp_temp_list
        return temp_list

    def get_line_from_block(self, angle, block, label):
        for i in range(len(block)):
            block[i] = self.rotation(angle, block[i], 1)
        x_min = min(block[:,0])
        x_max = max(block[:,0])
        y_min = min(block[:,1])
        y_max = max(block[:,1])
        temp_list =[]
        re = True
        line_start = False
        line_mid = False
        for i in np.arange(x_min,x_max,self.interval):
            re = not re
            temp_temp_list = []
            for j in np.arange(y_min, y_max, self.interval):
                point_in_floor = self.rotation(angle, np.array([i, j]), 0)
                x_pixel, y_pixel = world2picture(point_in_floor,self.origin,self.resolution)
                if line_start:
                    if line_mid:
                        if x_pixel>=0 and x_pixel<self.size[0] and y_pixel<self.size[1] and y_pixel>=0:
                            if self.map_cost[y_pixel, x_pixel]>self.threshold and self.model.predict([point_in_floor])[0] == label:
                                temp_temp_list.pop(-1)
                                temp_temp_list.append(point_in_floor)
                                plt.plot(np.array(temp_temp_list)[len(temp_temp_list)-2:, 0], np.array(temp_temp_list)[len(temp_temp_list)-2:, 1],linewidth = 3, linestyle = '-',color = 'yellow')
                                continue
                        line_start=False
                        line_mid=False
                    else:
                        if x_pixel>=0 and x_pixel<self.size[0] and y_pixel<self.size[1] and y_pixel>=0:
                            if self.map_cost[y_pixel, x_pixel]>self.threshold and self.model.predict([point_in_floor])[0] == label:
                                temp_temp_list.append(point_in_floor)
                                plt.plot(np.array(temp_temp_list)[len(temp_temp_list)-2:,0],np.array(temp_temp_list)[len(temp_temp_list)-2:,1],linewidth = 3,linestyle = '-',color = 'yellow')
                                line_mid = True
                                continue
                        line_start=False
                        line_mid=False
                else:
                    if x_pixel>=0 and x_pixel<self.size[0] and y_pixel<self.size[1] and y_pixel>=0:
                        if self.map_cost[y_pixel, x_pixel]>self.threshold and self.model.predict([point_in_floor])[0] == label:
                            temp_temp_list.append(point_in_floor)
                            line_start = True
            if re:
                temp_temp_list.reverse()
            temp_list+=temp_temp_list
            line_start=False
            line_mid=False
        return temp_list



    def cluster(self):
        # y_pred = KMeans(n_clusters=self.block_num, init='k-means++').fit_predict(self.refer_location)
        # for i in range(self.block_num):
        #     self.block_list.append(self.refer_location[y_pred==i])
        X=self.refer_location[:,:2]
        dpgmm = mixture.BayesianGaussianMixture(n_components=self.block_num,
                                                covariance_type='full').fit(X)
        label = dpgmm.predict(X)

        self.plot_results(X, label, dpgmm.means_, dpgmm.covariances_, 1,
                     'Bayesian Gaussian Mixture with a Dirichlet process prior')
        for i in range(self.block_num):
            if len(X[label[:]==i])>0:
                self.block_list.append(X[label[:]==i])
                self.block_center_list.append(dpgmm.means_[i])
                self.block_angle_list.append(self.covariances2angle(dpgmm.covariances_[i]))
        self.current_block_num = len(self.block_center_list)
    def find_cluster(self, point):
        dis = 10000
        index = 0
        for i in range(self.current_block_num):
            temp_dis = np.linalg.norm(point-self.block_center_list[i])
            if temp_dis<=dis:
                dis=temp_dis
                index =i
        self.block_list[index].insert(0,point)
        return index
    def sort_inner(self):
        for i in range(self.current_block_num):
            adjacent = self.dist_matrix_get(self.block_list[i],dist_type='eu')
            temp_order = self.TSP(adjacentMat=adjacent,best=1, time=3)
            self.block_list[i]=self.list_pick(self.block_list[i],temp_order)
    def sort_outter(self):
        adjacent = self.dist_matrix_get(self.block_center_list[:],dist_type='eu')
        temp_order = self.TSP(adjacentMat=adjacent,best=1)
        temp_order.pop(-1)

        self.block_center_list = self.list_pick(self.block_center_list,temp_order)
        self.block_list = self.list_pick(self.block_list,temp_order)
        self.block_angle_list = self.list_pick(self.block_angle_list, temp_order)
    def sort_whole(self):
        temp_list = []
        for i in range(self.current_block_num):
            temp_list += self.block_list[i]

        adjacent = self.dist_matrix_get(temp_list, dist_type='eu')
        temp_order = self.TSP(adjacentMat=adjacent, best=1, time=30)
        self.final_list_static = self.list_pick(temp_list, temp_order)

    def list_pick(self, main_list, indexes):
        return [main_list[x] for x in indexes]
    def line_extract(self):
        static_length = len(self.final_list_static)
        orient = mt.atan2(self.final_list_static[1, 1] - self.final_list_static[0, 1], self.final_list_static[1, 0] - self.final_list_static[0, 0])
        start_index = 0
        listNew = []
        for i in range(1, static_length - 1):
            if mt.atan2(self.final_list_static[i + 1, 1] - self.final_list_static[i, 1], self.final_list_static[i + 1, 0] - self.final_list_static[i, 0]) == orient:
                if i + 1 == static_length - 1:
                    listNew.append(self.final_list_static[start_index, :])
                    listNew.append(self.final_list_static[i + 1, :])
                else:
                    pass
            else:
                listNew.append(self.final_list_static[start_index, :])
                listNew.append(self.final_list_static[i, :])
                start_index = i
                orient = mt.atan2(self.final_list_static[i + 1, 1] - self.final_list_static[i, 1], self.final_list_static[i + 1, 0] - self.final_list_static[i, 0])
                if i + 1 == static_length - 1:
                    listNew.append(self.final_list_static[i + 1, :])
        listNew = np.array(listNew)
        for i in range(len(listNew) - 1):
            if (listNew[i, :] == listNew[i + 1, :]).all():
                listNew[i, 0] = 0
        listNew = listNew[listNew[:, 0] != 0]
        self.final_list_mobile = listNew
    def process(self):
        self.cluster()
        print('cluster '+str(self.current_block_num))
        start_index = self.find_cluster(self.start_point)
        self.right_shift(self.block_list,start_index)
        self.right_shift(self.block_center_list, start_index)
        self.sort_outter()
        print('sort_outter over')

        self.sort_inner()
        print('sort_inner over')
        self.divide_combine()
    def process_static(self):
        self.cluster_block()
        print('cluster ' + str(self.current_block_num))
        start_index = self.find_cluster(self.start_point)
        self.right_shift(self.block_list, start_index)
        self.right_shift(self.block_center_list, start_index)
        self.sort_outter()
        print('sort_outter over')
        # self.sort_whole()
        for i in range(self.current_block_num):
            self.final_list_static+=self.block_list[i]
        self.final_list_static.append(self.final_list_static[0])
        print('sort_whole over')

    def process_mobile(self):
        self.cluster_block(type=1)
        print('cluster ' + str(self.current_block_num))
        start_index = self.find_cluster(self.start_point)
        self.right_shift(self.block_list, start_index)
        self.right_shift(self.block_center_list, start_index)
        self.sort_outter()
        print('sort_outter over')
        for i in range(self.current_block_num):
            self.final_list_mobile+=self.block_list[i]
        self.final_list_mobile.append(self.final_list_mobile[0])



    def covariances2angle(self,covariances):
        v, w = linalg.eigh(covariances)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        angle = np.arctan(u[1] / u[0])
        # angle = 180. * angle / np.pi  # convert to degrees
        # angle = 90+ angle
        return angle
    def get_all_grid(self):
        for i in range(0,len(self.map_cost)):
            for j in range(0,len(self.map_cost[0])):
                if self.map_cost[i][j]>self.threshold:
                    x = j*self.resolution+self.origin[0]
                    y = i*self.resolution+self.origin[1]
                    self.white_area.append([x,y])

    def rotation(self, theta, P, type):
        R = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        if type==0:
            return np.matmul(R, P)
        else:
            return np.matmul(np.transpose(R), P)

    def plot_results(self, X, Y_, means, covariances, index, title):
        splot = plt.subplot(1, 1, 1)
        for i, (mean, covar, color) in enumerate(zip(
                means, covariances, color_iter)):
            v, w = linalg.eigh(covar)
            v = 2. * np.sqrt(2.) * np.sqrt(v)
            u = w[0] / linalg.norm(w[0])
            # as the DP will not use every component it has access to
            # unless it needs it, we shouldn't plot the redundant
            # components.
            if not np.any(Y_ == i):
                continue
            plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)
            block = X[Y_ == i, :]
            # Plot an ellipse to show the Gaussian component
            angle = np.arctan(u[1] / u[0])

            for i in range(len(block)):
                block[i] = self.rotation(angle, block[i], 1)
            x_min = min(block[:, 0])
            x_max = max(block[:, 0])
            y_min = min(block[:, 1])
            y_max = max(block[:, 1])
            width = x_max-x_min
            height = y_max-y_min
            point = np.array([x_min,y_min])
            point = self.rotation(angle, point,type=0)

            angle = 180. * angle / np.pi  # convert to degrees
            ell = mpl.patches.Rectangle(point, width, height, angle, color=color)
            ell.set_clip_box(splot.bbox)
            ell.set_alpha(0.5)
            splot.add_artist(ell)

        plt.xticks(())
        plt.yticks(())
        #plt.title(title)




if __name__ == '__main__':
  # main()
  # list = np.loadtxt("list.txt", dtype=float, delimiter=' ')[:,:2]
  # ruote = np.loadtxt("ruote.csv", dtype=int, delimiter=',')
  # list = list[ruote, :]
  # list = list[ruote, :]
  # plt.figure()
  # plt.plot(list[:, 0], list[:, 1], '-r.')
  # np.savetxt("static.csv", np.array(list), fmt='%f', delimiter=',', newline='\r\n')

  # np.savetxt("mobile.csv", np.array(listNew), fmt='%f', delimiter=',', newline='\r\n')
  # #plt.plot(list[:, 0], list[:, 1], '-b.')
  #
  # plt.figure()
  # plt.plot(listNew[:, 0], listNew[:, 1], '-r.')
  #
  # plt.xticks([])
  # plt.yticks([])
  # plt.axis('off')
  # plt.show()
  point3 = np.array([37, 75])
  point6 = np.array([21, 1.5])



  cover = Cover('./6b/map/mymap.yaml', 4, 0.8, point6)

  cover.process_static()
  for angle,center in zip(cover.block_angle_list, cover.block_center_list):
      print(center)
      print(angle)

  # plt.axis([- 5, 53, - 5, 80])
  # np.savetxt("list_6F_static.txt", np.array(cover.final_list_static), fmt='%f', delimiter=' ', newline='\r\n')
  print(len(cover.final_list_static))
  del cover.final_list_static[-1]
  del cover.final_list_static[0]
  for i in cover.final_list_static:
      plt.plot(i[0], i[1], 'r*', ms=10)
      plt.pause(0.01)




  # cover2 = Cover('./6F/map/mymap.yaml', 1, 0.8, point6)
  #
  # cover2.process_mobile()
  # for angle, center in zip(cover2.block_angle_list, cover2.block_center_list):
  #   print(center)
  #   print(angle)
  # alist = np.array(cover2.final_list_mobile)
  # plt.plot(alist[:, 0], alist[:, 1], 'r*',ms = 10)
  # np.savetxt("list_6F_mobile.txt", np.array(cover2.final_list_mobile), fmt='%f', delimiter=' ', newline='\r\n')
  # model = SpectralClustering(n_clusters=3, gamma=0.1)
  # X = np.array(cover.white_area)
  # # X = X[range(0,len(X),4),:]
  # y_pre = model.fit_predict(X)
  # plt.figure()
  # for i,(color) in enumerate(zip(color_iter)):
  #     plt.scatter(X[y_pre[:]==i,0], X[y_pre[:]==i,1], color=color)
  #     if i==2:
  #         break
  plt.show()

