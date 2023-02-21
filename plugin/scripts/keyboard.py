import socket
import getch
import sys, termios, tty, os

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


IP_ADDRESS = "192.168.0.112"  # replace with the IP address of your ESP32
PORT = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

while True:
    input_action = getch()

    if input_action == "w":
        action = str(0.0) + '\n' + str(200.0) + '\n'
        client_socket.sendall(action.encode())
        print("throttle")

    if input_action == "d":
        action = str(30.0) + '\n' +  str(200.0) + '\n'
        client_socket.sendall(action.encode())
        print("sterring")