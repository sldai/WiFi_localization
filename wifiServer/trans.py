#!/usr/bin/env python
# -*-coding:utf-8 -*- 
'''
@author: daishilong
@contact: daishilong1236@gmail.com
'''
#coding=utf-8
import paramiko, os
import cv2
import numpy as np
def remote_scp(type, host_ip, remote_path, local_path, username, password):
    ssh_port = 22
    try:
        conn = paramiko.Transport((host_ip, ssh_port))
        conn.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(conn)
        if type == 'remoteRead':
            if not local_path:
                fileName = os.path.split(remote_path)
                local_path = os.path.join('/tmp', fileName[1])
            sftp.get(remote_path, local_path)

        if type == "remoteWrite":
            sftp.put(local_path, remote_path)

        conn.close()
        return True

    except Exception:
        return False

host_ip = '39.105.14.245'
remote_path = '/root/wifiposition/list.txt'
local_path = 'list.txt'
username = 'root'
password = 'caonima@250'
if __name__ == '__main__':
    mymap = cv2.imread('template.jpg')
    mymap = np.array(mymap)
    mymap = mymap[::-1]
    mymap = cv2.cvtColor(mymap, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('template.jpg',mymap)
    remote_scp("remoteWrite", host_ip, remote_path, local_path, username, password )