#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf

def initial_pos_pub():
    rospy.init_node('initial_pos_pub', anonymous=True)
    publisher = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
    
    #Creating the message with the type PoseWithCovarianceStamped
    start_pos = PoseWithCovarianceStamped()
    #filling header with relevant information
    start_pos.header.frame_id = "map"
    #start_pos.header.stamp = rospy.Time.now()
    #filling payload with relevant information gathered from subscribing
    # to initialpose topic published by RVIZ via rostopic echo initialpose
    start_pos.pose.pose.position.x = 2
    start_pos.pose.pose.position.y = 2
    start_pos.pose.pose.position.z = 0.0

    th=0
    odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
    start_pos.pose.pose.orientation.x = odom_quat[0]
    start_pos.pose.pose.orientation.y = odom_quat[1]
    start_pos.pose.pose.orientation.z = odom_quat[2]
    start_pos.pose.pose.orientation.w = odom_quat[3]
    

    start_pos.pose.covariance[0] = 1
    start_pos.pose.covariance[7] = 1
    start_pos.pose.covariance[1:7] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
    start_pos.pose.covariance[8:34] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
    start_pos.pose.covariance[35] = 1

    rospy.loginfo(start_pos)
    #publisher.publish(start_pos)
    r = rospy.Rate(0.5)
    r.sleep()
    publisher.publish(start_pos)

if __name__ == '__main__':
    try:
        initial_pos_pub()
    except rospy.ROSInterruptException:
        pass