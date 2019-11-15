// Auto-generated. Do not edit!

// (in-package rosaria.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class BumperState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.front_bumpers = null;
      this.rear_bumpers = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('front_bumpers')) {
        this.front_bumpers = initObj.front_bumpers
      }
      else {
        this.front_bumpers = [];
      }
      if (initObj.hasOwnProperty('rear_bumpers')) {
        this.rear_bumpers = initObj.rear_bumpers
      }
      else {
        this.rear_bumpers = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BumperState
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [front_bumpers]
    bufferOffset = _arraySerializer.bool(obj.front_bumpers, buffer, bufferOffset, null);
    // Serialize message field [rear_bumpers]
    bufferOffset = _arraySerializer.bool(obj.rear_bumpers, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BumperState
    let len;
    let data = new BumperState(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [front_bumpers]
    data.front_bumpers = _arrayDeserializer.bool(buffer, bufferOffset, null)
    // Deserialize message field [rear_bumpers]
    data.rear_bumpers = _arrayDeserializer.bool(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += object.front_bumpers.length;
    length += object.rear_bumpers.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rosaria/BumperState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f81947761ff7e166a3bbaf937b9869b5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BumperState(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.front_bumpers !== undefined) {
      resolved.front_bumpers = msg.front_bumpers;
    }
    else {
      resolved.front_bumpers = []
    }

    if (msg.rear_bumpers !== undefined) {
      resolved.rear_bumpers = msg.rear_bumpers;
    }
    else {
      resolved.rear_bumpers = []
    }

    return resolved;
    }
};

module.exports = BumperState;
