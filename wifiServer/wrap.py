import numpy as np

data=np.loadtxt("E:/WiFi/实验室6楼/wifiData/行人验证/human.csv", dtype=float, delimiter=',')
wifiData=[]
for i in range(len(data)):
    if data[i,1]==2:
        wifiData.append(data[i,:])
wifiData=np.array(wifiData)
np.save('test_data.npy',wifiData[:,4:4+20])
np.save('test_label.npy',wifiData[:,2:2+2])