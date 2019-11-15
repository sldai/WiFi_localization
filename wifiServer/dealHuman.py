import numpy as np
path= "E:/WiFi/实验室6楼/wifiData/行人验证/11.15/pdr.csv"
data=np.loadtxt(path, dtype=float, delimiter=',')
cood=[]
index=[]
width,lenth=data.shape

for i in range(width):
    if data[i,1]==0:
        cood.append([data[i,0],data[i,2],data[i,3]])
        index.append(i)

for i in range(len(cood)-1):
    time=cood[i+1][0]-cood[i][0]
    speed_x=(cood[i+1][1]-cood[i][1])/time
    speed_y=(cood[i+1][2]-cood[i][2])/time
    for j in range(index[i],index[i+1]):
        data[j,2]=speed_x*(data[j,0]-cood[i][0])+cood[i][1]
        data[j, 3] = speed_y * (data[j, 0] - cood[i][0]) + cood[i][2]

np.savetxt(path,data,fmt='%f',delimiter=',',newline='\r\n')


