#!/usr/bin/env python3
# Import the necessary libraries
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


# Initialize the ROS node  
rospy.init_node("ip_camera_publisher", anonymous=True)
# Initialize the publisher
pub = rospy.Publisher("/camera/image", Image, queue_size=20)
# read the ip address from the yamel file
url = rospy.get_param("ip")+":81/stream"

# Continuously read frames from the IP camera stream
while not rospy.is_shutdown():

    # read frames from the IP camera stream
    cap = cv2.VideoCapture(url)

    # check if it is still streaming 
    while cap.isOpened():
        try:    
            # read a frame
            ret, frame = cap.read()
            # check if there is truely an image
            if ret:
                # convert the image from cv2 to a ros image message 
                image = CvBridge().cv2_to_imgmsg(frame, "bgr8")
                # publish the image
                pub.publish(image)
        except cv2.error as e:
            continue


#----------------------------------------------------------------------------------------------------------------------------



#!/usr/bin/env python3
# Import the necessary libraries
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import threading
import queue
# import numpy as np


def read_frame(cap, queue):
    while cap.isOpened():
        try:    
            ret, frame = cap.read()
            if not ret:
                break
            if queue.full():
                queue.get()
            queue.put(frame)
        except cv2.error as e:
            continue

def main(url):
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    my_queue = queue.Queue(maxsize=10)
    for _ in range (10):
        t = threading.Thread(target=read_frame, args=(cap, my_queue))
        t.daemon = True
        t.start()
    while True:
        frame = my_queue.get()
        # Convert the image to a ROS message
        ros_image = CvBridge().cv2_to_imgmsg(frame, "bgr8")
        # Publish the image to a ROS topic
        pub.publish(ros_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()


# Initialize the ROS node and the publisher 
rospy.init_node("ip_camera_publisher", anonymous=True)
pub = rospy.Publisher("/camera/image", Image, queue_size=20)

# Continuously read frames from the IP camera stream
while not rospy.is_shutdown():
    try:
        main("http://192.168.43.213:81/stream")
    except cv2.error as e:
        continue


    # try:
    #     # Open the IP camera stream
    #     cap = cv2.VideoCapture("http://192.168.43.213:81/stream")

    #     # increasing the buffer size
    #     # cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    #     while cap.isOpened():
    #         try:
    #             ret, frame = cap.read()
    #             if ret:
    #                 # Call the callback function with the latest frame
    #                 # Convert the image to a ROS message
    #                 ros_image = CvBridge().cv2_to_imgmsg(frame, "bgr8")

    #                 # Publish the image to a ROS topic
    #                 pub.publish(ros_image)
    #         except cv2.error as e:
    #             continue
    # except cv2.error as e:
    #     continue


