#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from socket import *
import tf
import threading
import time

def talker(client):
    
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        print('Waiting for connection...')
        data,addr = udpServer.recvfrom(bufsize)
        data  = data.decode(encoding='utf-8').upper()
        rospy.loginfo(data)
        data=data.split(',')
        for i in range(len(data)):
            data[i]=float(data[i])
        try:
            result=movebase_client(data[0],data[1],client)
            if result:
                rospy.loginfo("Goal execution done!")
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
            
        rate.sleep()


def movebase_client(x,y,client):

    #client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0
    
    th=0
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
    goal.target_pose.pose.orientation.x = odom_quat[0]
    goal.target_pose.pose.orientation.y = odom_quat[1]
    goal.target_pose.pose.orientation.z = odom_quat[2]
    goal.target_pose.pose.orientation.w = odom_quat[3]

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def registerServer():
    regStr = 'I am server'
    print(regStr)
    udpServer.sendto(regStr.encode(encoding='utf-8'),(brainIp,brainPort) )
    interMax = 10
    global timer
    timer = threading.Timer(interMax, registerServer)
    timer.start()



if __name__ == '__main__':  
    host = '' #listen to all ip
    brainIp = '39.105.14.245'
    #brainIp = '10.130.203.81'
    port = 8085 #port must equal
    brainPort = 8080
    bufsize = 1024
    addr = (host,port)
    udpServer = socket(AF_INET,SOCK_DGRAM)
    udpServer.bind(addr) #start to listen
    rospy.init_node('send_service_py')
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    registerServer()
    timer = threading.Timer(1.0, registerServer)
    timer.start()
    talker(client)
    goneStr = 'server gone'
    print(goneStr)
    udpServer.sendto(goneStr.encode(encoding='utf-8'),(brainIp,brainPort) )

        