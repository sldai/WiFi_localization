#include "ros/ros.h"
#include "nav_msgs/Odometry.h"

/**
 * This tutorial demonstrates simple receipt of position and speed of the Evarobot over the ROS system.
 */

/**
 * Callback function executes when new topic data comes.
 * Task of the callback function is to print data to screen.
 */
void chatterCallback(const nav_msgs::Odometry::ConstPtr& msg)
{
  ROS_INFO("Seq: [%d]", msg->header.seq);
  ROS_INFO("Position-> x: [%f], y: [%f], z: [%f]", msg->pose.pose.position.x,msg->pose.pose.position.y, msg->pose.pose.position.z);
  ROS_INFO("Orientation-> x: [%f], y: [%f], z: [%f], w: [%f]", msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
  ROS_INFO("Vel-> Linear: [%f], Angular: [%f]", msg->twist.twist.linear.x,msg->twist.twist.angular.z);
}

int main(int argc, char **argv)
{
  
  ros::init(argc, argv, "odom_listener");

  ros::NodeHandle n;

  
  ros::Subscriber sub = n.subscribe("odom", 1000, chatterCallback);

  
  ros::spin();

  return 0;
}
