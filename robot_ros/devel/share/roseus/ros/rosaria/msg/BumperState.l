;; Auto-generated. Do not edit!


(when (boundp 'rosaria::BumperState)
  (if (not (find-package "ROSARIA"))
    (make-package "ROSARIA"))
  (shadow 'BumperState (find-package "ROSARIA")))
(unless (find-package "ROSARIA::BUMPERSTATE")
  (make-package "ROSARIA::BUMPERSTATE"))

(in-package "ROS")
;;//! \htmlinclude BumperState.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass rosaria::BumperState
  :super ros::object
  :slots (_header _front_bumpers _rear_bumpers ))

(defmethod rosaria::BumperState
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:front_bumpers __front_bumpers) (let (r) (dotimes (i 0) (push nil r)) r))
    ((:rear_bumpers __rear_bumpers) (let (r) (dotimes (i 0) (push nil r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _front_bumpers __front_bumpers)
   (setq _rear_bumpers __rear_bumpers)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:front_bumpers
   (&optional __front_bumpers)
   (if __front_bumpers (setq _front_bumpers __front_bumpers)) _front_bumpers)
  (:rear_bumpers
   (&optional __rear_bumpers)
   (if __rear_bumpers (setq _rear_bumpers __rear_bumpers)) _rear_bumpers)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; bool[] _front_bumpers
    (* 1    (length _front_bumpers)) 4
    ;; bool[] _rear_bumpers
    (* 1    (length _rear_bumpers)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; bool[] _front_bumpers
     (write-long (length _front_bumpers) s)
     (dotimes (i (length _front_bumpers))
       (if (elt _front_bumpers i) (write-byte -1 s) (write-byte 0 s))
       )
     ;; bool[] _rear_bumpers
     (write-long (length _rear_bumpers) s)
     (dotimes (i (length _rear_bumpers))
       (if (elt _rear_bumpers i) (write-byte -1 s) (write-byte 0 s))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; bool[] _front_bumpers
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _front_bumpers (make-list n))
     (dotimes (i n)
     (setf (elt _front_bumpers i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;; bool[] _rear_bumpers
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _rear_bumpers (make-list n))
     (dotimes (i n)
     (setf (elt _rear_bumpers i) (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
     ))
   ;;
   self)
  )

(setf (get rosaria::BumperState :md5sum-) "f81947761ff7e166a3bbaf937b9869b5")
(setf (get rosaria::BumperState :datatype-) "rosaria/BumperState")
(setf (get rosaria::BumperState :definition-)
      "Header header
bool[] front_bumpers
bool[] rear_bumpers

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :rosaria/BumperState "f81947761ff7e166a3bbaf937b9869b5")


