#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from socket import *
from time import ctime
from particleFilterClass import particleFilter
import numpy as np
import math as mt
import os,sys
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf

def initialpos_pub():
    #Creating the message with the type PoseWithCovarianceStamped
    start_pos = PoseWithCovarianceStamped()
    #filling header with relevant information
    start_pos.header.frame_id = "map"
    #start_pos.header.stamp = rospy.Time.now()
    #filling payload with relevant information gathered from subscribing
    # to initialpose topic published by RVIZ via rostopic echo initialpose
    mean = pF.getMean()
    start_pos.pose.pose.position.x = mean[0]
    start_pos.pose.pose.position.y = mean[1]
    start_pos.pose.pose.position.z = 0

    th=mean[2]
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
    start_pos.pose.pose.orientation.x = odom_quat[0]
    start_pos.pose.pose.orientation.y = odom_quat[1]
    start_pos.pose.pose.orientation.z = odom_quat[2]
    start_pos.pose.pose.orientation.w = odom_quat[3]
    
    

    start_pos.pose.covariance[0] = 0.25
    start_pos.pose.covariance[7] = 0.25
    start_pos.pose.covariance[1:7] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
    start_pos.pose.covariance[8:34] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
    start_pos.pose.covariance[35] = 0.25

    rospy.loginfo(start_pos)
    publisher.publish(start_pos)
    sys.exit()


def callbackOdom(odom):
    #rospy.loginfo(rospy.get_caller_id()+"I heard %s",odom)
    #print(odom.twist.twist.angular.x)
    global current_time,last_time
    current_time=odom.header.stamp
    if last_time==0:
        last_time=current_time
        return
    dt=(current_time-last_time).to_sec()
    last_time=current_time
    movement=[odom.twist.twist.linear.x*dt,odom.twist.twist.linear.y*dt,odom.twist.twist.angular.z*dt]
    move_list.append([int(str(current_time)), odom.twist.twist.linear.x*dt, odom.twist.twist.linear.y*dt, odom.twist.twist.angular.z*dt])
    if ifIni==True:
        move(movement)
        print("move")
    

def callbackWifi(data):
    gettedData=data.data
    gettedData=str(rospy.Time.now())+gettedData
    gettedData = gettedData.split(',')
    observe=range(len(gettedData))
    for i in range(len(gettedData)):
        observe[i] = int(gettedData[i])
    wifi_list.append(observe)
    print("wifi")
    update(observe)

def callbackOk(data):
    msg = data.data
    if msg=='ok':
        initialpos_pub()
    
def update(observe):
    global ifIni
    if ifIni==False:
        pF.particleInitial(pF.knn(observe[1:(1 + apNum)], 11), 100)
        ifIni=True
        print('start')
    elif ifIni:
        pF.particleUpdate(observe=observe[1:(1 + apNum)])
        if pF.ifResample(50)==1:
            pF.particleResample()
        print("update")

def move(step):
    pF.particleMoveRobot(step)  


def listener():  
    rospy.Subscriber("odom", Odometry, callbackOdom)
    rospy.Subscriber("chatter", String, callbackWifi)
    rospy.Subscriber("wifiInitialOk", String, callbackOk)
    rospy.spin()
    
    


apNum=20
pF = particleFilter(apNum, 'svm', sys.path[0]+'/6b')
ifIni = False
current_time=0
last_time=0
move_list=[]
wifi_list=[]
if __name__ == '__main__':
    rospy.init_node('wifiPositioning', anonymous=True)
    publisher = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
    listener()
    
    wifi_array=np.array(wifi_list)
    
    move_array=np.array(move_list)
    #print(move_array)
    np.savetxt(sys.path[0]+"/wifi_list.csv",wifi_array,fmt='%f',delimiter=',',newline='\r\n')
    np.savetxt(sys.path[0]+"/move_list.csv",move_array,fmt='%f',delimiter=',',newline='\r\n')
