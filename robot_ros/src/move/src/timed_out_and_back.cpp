#include <ros/ros.h>
#include <signal.h>
#include <geometry_msgs/Twist.h>
#include <string.h>

ros::Publisher cmdVelPub;

void shutdown(int sig)
{
  cmdVelPub.publish(geometry_msgs::Twist());
  ROS_INFO("timed_out_and_back.cpp ended!");
  ros::shutdown();
}

int main(int argc, char** argv)
{

  ros::init(argc, argv, "go_and_back");
  std::string topic = "/cmd_vel";
  ros::NodeHandle node;
  //Publisher to control the robot's speed
  cmdVelPub = node.advertise<geometry_msgs::Twist>(topic, 1);

  //How fast will we update the robot's movement?
  double rate = 50;
  //Set the equivalent ROS rate variable
  ros::Rate loopRate(rate);

  //execute a shutdown function when exiting
  signal(SIGINT, shutdown);
  ROS_INFO("timed_out_and_back.cpp start...");

  //Set the forward linear speed to 0.2 meters per second
  float linear_speed = 0.2;

  //Set the travel distance to 1.0 meters
  float goal_distance = 1.0;

  //How long should it take us to get there?
  float linear_duration = goal_distance / linear_speed;

  //Set the rotation speed to 1.0 radians per second
  float angular_speed = 1.0;

  //Set the rotation angle to Pi radians (180 degrees)
  float goal_angle = M_PI;

  //How long should it take to rotate?
  float angular_duration = goal_angle / angular_speed;

  int count = 0;//Loop through the two legs of the trip
  int ticks;
  geometry_msgs::Twist speed; // 控制信号载体 Twist message
  while (ros::ok())
  {

    speed.linear.x = linear_speed; // 设置线速度，正为前进，负为后退
    // Move forward for a time to go 1 meter
    ticks = int(linear_duration * rate);
    for(int i = 0; i < ticks; i++)
    {
      cmdVelPub.publish(speed); // 将刚才设置的指令发送给机器人
      loopRate.sleep();
    }
    //Stop the robot before the rotation
    cmdVelPub.publish(geometry_msgs::Twist());
    //loopRate.sleep();
    ROS_INFO("rotation...!");

    //Now rotate left roughly 180 degrees
    speed.linear.x = 0;
    //Set the angular speed
    speed.angular.z = angular_speed; // 设置角速度，正为左转，负为右转
    //Rotate for a time to go 180 degrees
    ticks = int(angular_duration * rate);
    for(int i = 0; i < ticks; i++)
    {
       cmdVelPub.publish(speed); // 将刚才设置的指令发送给机器人
       loopRate.sleep();
    }
    speed.angular.z = 0;
    //Stop the robot before the next leg
    cmdVelPub.publish(geometry_msgs::Twist());

    count++;
    if(count == 2)
    {
      count = 0;
      cmdVelPub.publish(geometry_msgs::Twist());
      ROS_INFO("timed_out_and_back.cpp ended!");
      ros::shutdown();
    }
    else
    {
      ROS_INFO("go back...!");
    }
  }

  return 0;
}
