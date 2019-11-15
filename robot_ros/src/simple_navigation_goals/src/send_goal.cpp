#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include<iostream>
#include<fstream>
#include <unistd.h>
#include "std_msgs/String.h"
// %EndTag(MSG_HEADER)%
#include <time.h>
#include <sstream>
using namespace std;
time_t timep;
    
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
int seconds = 0;
int main(int argc, char** argv){
  ros::init(argc, argv, "simple_navigation_goals");
  ros::NodeHandle n;
  ofstream myfile;
  string storePath="/home/heinrich/temp/print_stop.txt";
  myfile.open(storePath.c_str(), ios::app);
  //tell the action client that we want to spin a thread by default
  MoveBaseClient ac("move_base", true);

  //wait for the action server to come up
  while(!ac.waitForServer(ros::Duration(5.0))){
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;

  //we'll send a goal to the robot to move 1 meter forward
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();
  float x[1000],y[1000];
  for(int i=0;i<1000;i++)
  {
    x[i]=0;
    y[i]=0;
  }
  ifstream cor("/home/heinrich/catkin_ws/coordinate/list_3F_mobile.txt");
  float temp_x,temp_y;
  int count;
  for(count=0;;count++)
  {
    cor>>temp_x>>temp_y;
    if(temp_x==0)
    {
      break;
    }
    x[count]=temp_x;
    y[count]=temp_y;
  }
  for(int c=0;c<1;c++)
  {
    for(int i=0;i<count;i++)
    {
      goal.target_pose.pose.position.x = x[i];
      goal.target_pose.pose.position.y = y[i];
      goal.target_pose.pose.orientation.w = 1.0;

      ROS_INFO("Sending goal");
      ac.sendGoal(goal);
  
      ac.waitForResult();
      if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
        ROS_INFO("Hooray, the base moved 1 meter forward");
      else
        ROS_INFO("The base failed to move forward 1 meter for some reason");
      time (&timep);
      myfile<<timep<<",1\n";
      sleep(seconds);
      // if(count==4)
      //   sleep(seconds); //wait
    }
    /*
    for(int i=count-1;i>=0;i--)
    {
      goal.target_pose.pose.position.x = x[i];
      goal.target_pose.pose.position.y = y[i];
      goal.target_pose.pose.orientation.w = 1.0;

      ROS_INFO("Sending goal");
      ac.sendGoal(goal);
  
      ac.waitForResult();
      if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
        ROS_INFO("Hooray, the base moved 1 meter forward");
      else
        ROS_INFO("The base failed to move forward 1 meter for some reason");
      // if(count==4)
      //   sleep(seconds); //wait
    }
    break;
    */
  }
  

  myfile.close();
  

  return 0;
}
