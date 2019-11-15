# p3dx_navigation
ROS package navigation to Pioneer P3-DX

## Install
- Clone the package folder

		$ cd ~/catkin_ws/src
		$ git clone https://github.com/LCAD-UFES/p3dx_navigation.git
		$ cd ..
		$ catkin_make

- Install rosaria

		$ cd ~/catkin_ws/src
		$ git clone https://github.com/amor-ros-pkg/rosaria.git
		$  cd ..
		$ catkin_make

- Install sicktoolbox-wrapper

		$ sudo apt-get install ros-{version}-sicktoolbox-wrapper

## Simulation
To run simulation

		$ roslaunch p3dx_navigation simulation.launch

and another terminal

		$ roslaunch p3dx_navigation move_base_gazebo.launch

## Real robot
1. Connect the pioneer in USB port, then the laser sick.

2. Open 3 terminal

		$ sudo chmod 777 /dev/ttyUSB*
                $ sudo chmod 777 /dev/ttyACM*
                $ rosrun hokuyo_node hokuyo_node
		$ roslaunch p3dx_navigation pioneer.launch
		#$ roslaunch p3dx_navigation rviz_p3dx.launch
		$ roslaunch p3dx_navigation move_base_rosaria.launch
		$ rosrun p3dx_navigation getc
                $ rosrun p3dx_navigation talker.py
                $ rosrun simple_navigation_goals send_goal



---

Learn more about using the ROS navigation stack at http://wiki.ros.org/navigation
