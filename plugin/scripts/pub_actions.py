import socket
import rospy
from std_msgs.msg import String

def socket_to_ros():
    buffer = b''
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ("192.168.1.5", 1)
    sock.connect(server_address)

    # Initialize the ROS node
    rospy.init_node('socket_to_ros', anonymous=True)

    # Create a publisher to publish the received data to a ROS topic
    pub = rospy.Publisher('/socket_data', String, queue_size = 1)
    while not rospy.is_shutdown():
        
        # Receive data from the socket
        while b'\r\n' not in buffer:
            data = sock.recv(1024)
            buffer += data

        data,_,_ = buffer.partition(b'\r\n')
        
        vel_msg=String()
        vel_msg.data=data.decode()

        # Publish the received data to the ROS topic
        pub.publish(vel_msg)
        
if __name__ == '__main__':
    try:
        socket_to_ros()
    except rospy.ROSInterruptException:
        pass