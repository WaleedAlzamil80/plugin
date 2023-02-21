#!/usr/bin/env python3
# Import the necessary libraries
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge
from PIL import Image as PILImage
import requests
import concurrent.futures
import threading

# Initialize the ROS node and the publisher
rospy.init_node("ip_camera_publisher", anonymous=True)
pub = rospy.Publisher("/camera/image", Image, queue_size=20)
# lock = threading.Lock ( ) 

url ="http://192.168.0.130:81/stream"
# Open the IP camera stream
cap = cv2.VideoCapture(url)
def camera_video():
    ret, frame = cap.read()
    if ret:
    # Call the callback function with the latest frame
    # Convert the image to a ROS message
        # lock.acquire ( ) 
        ros_image = CvBridge().cv2_to_imgmsg(frame, "bgr8")
    # Publish the image to a ROS topic
        pub.publish(ros_image)
        # lock.release ()

# def camera_with_image(url):
#     #rate = rospy.Rate(100) # 10 Hz
#     img = PILImage.open(requests.get(url,verify=False, stream = True).raw)
#     img = np.array(img)
    
#     # Convert the image to a ROS image message
#     bridge = CvBridge()
#     # lock.acquire () 
#     ros_image = bridge.cv2_to_imgmsg(img, "bgr8")

#     # Publish the image message
#     pub.publish(ros_image)
#     # lock.release ()

while not rospy.is_shutdown():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(camera_video) for _ in range(10)]
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())

#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************
# # manually
# threads = []
# for _ in range(10):
#     t = threading.Thread(target=camera_video, args=[url])
#     t.start()
#     threads.append(t)
# for thred in threads:
#     thred.join()
# #-----------------------------------------------------------------
# # automatically
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = [executor.submit(camera_video, url) for _ in range(10)]
#     for f in concurrent.futures.as_completed(results):
#         print(f.result())
# #------------------------------------------------------------------

# class IPCamera(object):
#     def __init__(self, url):
#         try:
#             self.stream=urllib.urlopen(url)
#         except:
#             rospy.logerr('Unable to open camera stream: ' + str(url))
#             sys.exit() #'Unable to open camera stream')
#         self.bytes=''
#         self.image_pub = rospy.Publisher("/camera/image", Image, queue_size=10)
#         self.bridge = CvBridge()


# class IPCamera(object):
#     def __init__(self, url):
        
#         self.stream=requests.get(url)
#         self.bytes=''
#         self.image_pub = rospy.Publisher("/camera/image", Image, queue_size=10)
#         self.bridge = CvBridge()
        
# # Main
# if __name__ == '__main__':

#     parser = argparse.ArgumentParser(prog='ip_camera.py', description='reads a given url string and dumps it to a ros_image topic')

#     # Para visualizar la imagen capturada del LAN ip cam: $ rosrun camera_pkg publisher.py --gui
#     parser.add_argument('-g', '--gui', action='store_true', help='show a GUI of the camera stream')
#     # Definir la direccion ip agragando la url del stream en default o ejecutar en ventana de comandos : $rosrun camera_pkg publisher.py -u YOUR_CAMERA_URL --gui
#     parser.add_argument('-u', '--url', default='http://'+ IP_address+":81/stream" , help='camera stream url to parse')
#     args = parser.parse_args()
    
#     rospy.init_node('ip_camera_publisher', anonymous=True)
#     ip_camera = IPCamera(args.url)

#     while not rospy.is_shutdown():
#         ip_camera.bytes += ip_camera.stream.read(1024)
#         a = ip_camera.bytes.find('\xff\xd8')
#         b = ip_camera.bytes.find('\xff\xd9')
#         if a!=-1 and b!=-1:

#             jpg = ip_camera.bytes[a:b+2]
#             ip_camera.bytes= ip_camera.bytes[b+2:]
#             if len(jpg) >0:
#                 i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
#             image_message = i
#             ip_camera.image_pub.publish(ip_camera.bridge.cv2_to_imgmsg(image_message, "bgr8"))

#         if args.gui:
#             cv2.imshow('IP Camera Publisher Cam',i)
#         if cv2.waitKey(1) ==27: # wait until ESC key is pressed in the GUI window to stop it
# 	        exit(0) 

#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************

# # IPCamera classs
# class IPCamera(object):
#     def __init__(self):
#         self.bridge = CvBridge()
#         self.image_sub = rospy.Subscriber("/camera/image",Image,self.callback)

#     def callback(self,data):
#         try:
#           cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
#         except(CvBridgeError):

#           print("OOps")
#           # pass
#         cols,rows = cv_image.shape[:2]
        
#         # if (cols > 60 and rows > 60) :
#         #     cv2.circle(cv_image, (50,50), 10, 255)

#         cv2.imshow("ip_camera Listener Image", cv_image)
#         cv2.waitKey(3)

# # Main        
# if __name__ == '__main__':
#   ip_camera_listener = IPCamera()
#   rospy.init_node('ip_camera_subscriber', anonymous=True)
#   rospy.spin()
#   cv2.DestroyAllWindows()
