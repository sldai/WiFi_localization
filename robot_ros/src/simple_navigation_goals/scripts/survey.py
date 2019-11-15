#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import tf
from tf.transformations import quaternion_from_euler
import geometry_msgs.msg
import roslib
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import numpy as np
from detect_outlier import DetectOutlier
from signal_recover import SignalRecover
import math
class SmartSurvey:
    def __init__(self, survey_time, map_setting, target_list, record_path):
        self.listener = tf.TransformListener()
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        self.survey_time = survey_time
        self.map_setting = map_setting
        self.sojourn_time = 10
        self.survey_fg = []
        self.recover_fg = None
        self.outlier_fg = None
        self.target_list = target_list.tolist()
        self.target_once = target_list.tolist()
        self.record_path = record_path

        self.chatter_sub = None
        self.register_listener()

    def callback_chatter(self, data):
        # record fingerprints
        gettedData = data.data
        (trans, rot) = self.listener.lookupTransform('/map', '/base_link', rospy.Time(0))

        gettedData = str(rospy.Time.now().secs) +","+ str(trans[0]) + "," + str(trans[1]) + gettedData
        print(gettedData)
        gettedData = gettedData.split(',')
        observe = np.zeros(len(gettedData))
        for i in range(len(gettedData)):
            observe[i] = gettedData[i]
        self.survey_fg.append(observe)

    def register_listener(self):
        self.chatter_sub = rospy.Subscriber("chatter", String, self.callback_chatter)
    
    def unregister_listener(self):
        if self.chatter_sub != None:
            self.chatter_sub.unregister()

    def recover(self, raw_fg):
        tinker = SignalRecover(self.map_setting, raw_fg)
        tinker.recover_process()
        return tinker.GetResult()


    def detect_outlier(self, recover_fg):
        detector = DetectOutlier(recover_fg, self.map_setting, 2, self.target_list)
        detector.process()
        self.outlier_fg = detector.GetOutlierFingerprints()
        return detector.get_target_list()

    def send_goal(self,x,y,rot = 0):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        q = quaternion_from_euler(0, 0, rot)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]
        print("send goal "+ str(x) + "," +str(y))
        self.client.send_goal(goal)
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
        else:
            rospy.loginfo("reach goal")
            return self.client.get_result()

    def survey(self):
        last_target = self.target_once[0]
        for target in self.target_once:
            rot = math.atan2(target[1]-last_target[1], target[0]-last_target[0])
            self.send_goal(target[0], target[1], rot)
            last_target = target

    def resurvey(self):
        last_target = self.target_once[0]
        for target in self.target_once:
            rot = math.atan2(target[1]-last_target[1], target[0]-last_target[0])
            self.send_goal(target[0], target[1], rot)
            last_target = target
            rospy.sleep(self.sojourn_time)

    def run(self):
        print("run")
        for i in range(self.survey_time):
            if i == 0:
                self.survey()
            else:
                self.resurvey()
            np.savetxt(self.record_path + "/survey_points" + str(i) + ".csv", self.target_once, fmt='%f', delimiter=',',
                       newline='\r\n')
            np.savetxt(self.record_path+"/survey"+str(i)+".csv", np.array(self.survey_fg), fmt='%f', delimiter=',', newline='\r\n')
            self.recover_fg = self.recover(np.array(self.survey_fg))
            np.savetxt(self.record_path+"/recover"+str(i)+".csv", self.recover_fg, fmt='%f', delimiter=',', newline='\r\n')
            resurvey_target = self.detect_outlier(self.recover_fg)
            np.savetxt(self.record_path + "/outlier" + str(i) + ".csv", self.outlier_fg, fmt='%f', delimiter=',',
                       newline='\r\n')
            
            if len(resurvey_target) == len(self.target_list):
                break
            else:
                self.target_once = resurvey_target[len(self.target_list):]
                self.target_list = resurvey_target

    def run_sojourn(self):
        print("run")
        for i in range(1):
            self.resurvey()
            np.savetxt(self.record_path + "/survey_points" + str(i) + ".csv", self.target_once, fmt='%f', delimiter=',',
                       newline='\r\n')
            np.savetxt(self.record_path+"/survey"+str(i)+".csv", np.array(self.survey_fg), fmt='%f', delimiter=',', newline='\r\n')
            self.recover_fg = self.recover(np.array(self.survey_fg))
            np.savetxt(self.record_path+"/recover"+str(i)+".csv", self.recover_fg, fmt='%f', delimiter=',', newline='\r\n')
            resurvey_target = self.detect_outlier(self.recover_fg)
            np.savetxt(self.record_path + "/outlier" + str(i) + ".csv", self.outlier_fg, fmt='%f', delimiter=',',
                       newline='\r\n')
            
            if len(resurvey_target) == len(self.target_list):
                break
            else:
                self.target_once = resurvey_target[len(self.target_list):]
                self.target_list = resurvey_target

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        map_setting = {'ap_num': 19, 'interval': 0.8, 'origin': [0.0, 0.0], 'lost_signal': -100}
        
        # run sojourn
        # target_list_generated = np.loadtxt('/home/heinrich/catkin_ws/coordinate/list_3F_corridor_static.csv', dtype=float, delimiter=',')
        # survey_sojourn = SmartSurvey(1,map_setting,target_list_generated,"/home/heinrich/survey_results/3F_corridor/sojourn")
        # survey_sojourn.run_sojourn()
        # survey_sojourn.unregister_listener()

        # run test
        target_list_generated = np.loadtxt('/home/heinrich/catkin_ws/coordinate/list_3F_corridor_mobile.csv', dtype=float, delimiter=',')
        survey_test = SmartSurvey(1,map_setting,target_list_generated,"/home/heinrich/survey_results/3F_corridor/test")
        survey_test.run()
        survey_test.unregister_listener()
        
        # run fast survey
        target_list_generated = np.loadtxt('/home/heinrich/catkin_ws/coordinate/list_3F_corridor_mobile.csv', dtype=float, delimiter=',')
        survey_re = SmartSurvey(2,map_setting,target_list_generated,"/home/heinrich/survey_results/3F_corridor/survey")
        survey_re.run()
        survey_re.unregister_listener()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")