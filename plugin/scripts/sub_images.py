#!/usr/bin/env python3

# Import the necessary libraries
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Define a callback function to convert the ROS message to an image
def image_callback(ros_image):
  # convert the ROS message to an image
  img = CvBridge().imgmsg_to_cv2(ros_image, "bgr8")
  
# Initialize the ROS node 
rospy.init_node("ip_camera_subscriber", anonymous=True)
# Initialize the subscriber
sub = rospy.Subscriber("/camera/image", Image, image_callback)

# Keep the ROS node running
rospy.spin()