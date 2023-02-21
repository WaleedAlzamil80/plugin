#!/usr/bin/env python3
import socket
import rospy
from std_msgs.msg import Float64MultiArray

IP_ADDRESS = "192.168.8.136"  # replace with the IP address of your ESP32
PORT = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

rospy.init_node("car_control")

# actions [0] steering_angle
# actions [1] throttle

actions = Float64MultiArray()
actions.data = [0.0, 0.0]
      
def actions_callback(data:Float64MultiArray):
    global actions
    print("message")
    actions.data[0] = data.data[0]
    actions.data[1] = data.data[1]
    message = str(actions.data[0])  + '\n' +  str(actions.data[1]) + '\n'
    client_socket.sendall(message.encode())

rospy.Subscriber("/control_actions", Float64MultiArray, actions_callback)
rospy.spin()