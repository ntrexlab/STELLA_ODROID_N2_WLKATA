#! /usr/bin/env python

import time
import rospy
import cv2
import os

from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError

if __name__=="__main__":
    cap = cv2.VideoCapture('/dev/C920')
    camera_info = CameraInfo()

    rospy.init_node('stella_camera_node')
    bridge = CvBridge()
    pub = rospy.Publisher('camera', Image, queue_size=1)
    pub_wlkata = rospy.Publisher('camera_for_wlkata',Image,queue_size=1)
    pub_info = rospy.Publisher('camera/info',CameraInfo, queue_size=1)
    rate = rospy.Rate(10)

    try:
        while not rospy.is_shutdown():
            ref,frame = cap.read()
            if not ref:
                rospy.loginfo("Not Found Devices")
                break
            image_msg = bridge.cv2_to_imgmsg(frame,"bgr8")
            pub.publish(image_msg)
            frame = cv2.circle(frame,(320,675),350,(255,0,0),3)
            image_msg = bridge.cv2_to_imgmsg(frame,"bgr8")
            camera_info.width = 640
            camera_info.height = 480
            camera_info.distortion_model = 'plumb_bob'
            camera_info.K = [624.4456808313446, 0.0, 303.7012143829713, 0.0, 625.1485146237704, 171.8339191749146, 0.0, 0.0, 1.0]
            camera_info.D = [-0.03009146532457465, 0.06562638735614496, -0.006918955305431058, -0.01201401550740573, 0.0]
            camera_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
            camera_info.P = [622.6001586914062, 0.0, 296.9734834036681, 0.0, 0.0, 627.5858154296875, 169.1584594550695, 0.0, 0.0, 0.0, 1.0, 0.0]
            pub_info.publish(camera_info)
            rate.sleep()

    except KeyboardInterrupt:
        rospy.loginfo("Exiting Program")

    except Exception as exception_error:
        rospy.loginfo("Error occurred. Exiting Program")
        rospy.loginfo("Error: " + str(exception_error))

    finally:
        cap.release()
        pass

