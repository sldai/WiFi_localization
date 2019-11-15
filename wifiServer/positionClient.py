# --
from socket import *
from time import ctime
from particleFilterClass import particleFilter
import numpy as np
import math as mt
from clientClass import client

theta0 = 180
apNum = 20


def addClient(ip):
    newClient = client(ip, apNum, 'svm', './6b', theta0)
    client_list.append(newClient)


def findClientIndexByIp(ip):
    for i in range(len(client_list)):
        if ip == client_list[i].ip:
            index = i
            return index
    return -1


def clientUpdate(ip, data):
    thisClient = client_list[findClientIndexByIp(ip)]
    if not thisClient.ifIni:
        if data[0] == 0:
            thisClient.clientIni(data)
            mean = thisClient.getMean()
            meanStr = '' + str(mean[0]) + ',' + str(mean[1])
            udpServer.sendto(meanStr.encode(encoding='utf-8'), ip)
    else:
        thisClient.update(data)
        mean = thisClient.getMean()
        meanStr = '' + str(mean[0]) + ',' + str(mean[1])
        udpServer.sendto(meanStr.encode(encoding='utf-8'), ip)


def removeClient(ip):
    index = findClientIndexByIp(ip)
    overStr = 'over'
    udpServer.sendto(overStr.encode(encoding='utf-8'), ip)
    del client_list[index]

def addServer(ip):
    server_list.append(ip)

def sendReq(ip):
    thisClient = client_list[findClientIndexByIp(ip)]
    mean = thisClient.getMean()
    meanStr = '' + str(mean[0]) + ',' + str(mean[1])
    if len(server_list)>=1:
        udpServer.sendto(meanStr.encode(encoding='utf-8'), server_list[0])
    else:
        print('no server')


if __name__ == "__main__":
    host = ''  # 监听所有的ip
    port = 8080  # 接口必须一致
    bufsize = 1024
    addr = (host, port)

    client_list = []
    server_list = []
    udpServer = socket(AF_INET, SOCK_DGRAM)
    udpServer.bind(addr)  # 开始监听

    while True:
        print('Waiting for connection...')

        gettedData, clientAddr = udpServer.recvfrom(bufsize)  # 接收数据和返回地址
        gettedData = gettedData.decode(encoding='utf-8')
        if gettedData == 'start':
            addClient(clientAddr)
            print('there '+str(len(client_list))+' clients')
        elif gettedData == 'over':
            removeClient(clientAddr)
            print('there '+str(len(client_list))+' clients')
        elif gettedData == 'I am server':
            addServer(clientAddr)
        elif gettedData == 'service request':
            sendReq(clientAddr)
        else:
            data = gettedData.split(',')
            for i in range(len(data)):
                data[i] = float(data[i])
            clientUpdate(clientAddr,data)





