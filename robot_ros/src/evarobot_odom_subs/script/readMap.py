import yaml
import matplotlib.pyplot as plt
import numpy as np
import math as mt
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
if __name__ == '__main__':
    f = open("./6b/map/mymap.yaml")
    temp = yaml.load(f)
    resolution = temp['resolution']
    map_origin = temp['origin']
    mapData = read_ros_map('./6b/map/mymap.pgm')
    list = []
    for y in range(-6, 74):
        for x in range(0, 51):
            x_pixel = int(mt.floor((x - map_origin[0]) / resolution))
            y_pixel = int(mt.floor((y - map_origin[1]) / resolution))
            if mapData[y_pixel, x_pixel] > 225:
                list.append([x, y])
                plt.plot(x, y, 'ro')
    np.savetxt("list.txt", np.array(list), fmt='%f', delimiter=' ', newline='\r\n')
    plt.show()






