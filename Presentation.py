"""
DJI tello edu Presentation - Dan-Brooks

This is a DJI tello project created for the autonomous systems course in university
The purpose of this code was to demonstrate the autonomous capabilities of the DJI tello

Requirements
- OpenCV
- threading

SDK INFO
-https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf
- IP 192.168.10.1
- UDP PORT 8889
- VIDEO PORT 11111

"""

import time
from time import sleep
import cv2
import socket
from threading import Thread

# Network Configuration
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_VIDEO_PORT = 11111
bufferSize = 1024

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (TELLO_IP, TELLO_PORT)

# Send command to tello and receive a response
def send_command(command):
    sock.sendto(command.encode('utf-8'), tello_address)
    msg = sock.recvfrom(bufferSize)
    return msg

#first command to tello
msg = send_command("command")
print(msg)

#This function demonstrates some basic movement capabilities of the drone
def task1():
    msg = send_command("takeoff")
    print(msg)
    msg = send_command("up 30")
    print(msg)
    msg = send_command("forward 20")
    print(msg)
    msg = send_command("cw 180")
    print(msg)
    msg = send_command("back 20")
    print(msg)
    msg = send_command("ccw 180")
    print(msg)
    msg = send_command("curve 60 -60 0 0 -120 0 20")
    print(msg)
    msg = send_command("cw 180")
    print(msg)
    msg = send_command("curve 60 60 0 0 120 0 20")
    print(msg)

#This function demonstrates more advanced movement and give statistic information
def task2():
    msg = send_command("takeoff")
    print(msg)
    msg = send_command("flip l")
    print(msg)
    msg = send_command("flip r")
    print(msg)
    msg = send_command("speed?")
    print(msg)
    msg = send_command("speed 30")
    print(msg)
    msg = send_command("speed?")
    print(msg)
    msg = send_command("battery?")
    print(msg)
    msg = send_command("time?")
    print(msg)
    msg = send_command("height?")
    print(msg)
    msg = send_command("land")
    print(msg)

#This function allows a stream of the operations to viewed
def task3():
    msg = send_command("streamon")
    print(msg)

    cap = cv2.VideoCapture(f'udp://{TELLO_IP}:{TELLO_VIDEO_PORT}')


    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('tello Video Stream', frame)

            cv2.imshow('img1', frame)  # display the captured image
            # press p to save the current frame
            if cv2.waitKey(1) & 0xFF == ord('p'):
                timestamp = int(time.time())
                filename = f"tello_photo_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"photo taken saved as {filename}")

            # press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        msg = send_command("streamoff")
        print(msg)
        sock.close()

#The threading allows the system to execute task 2 and 3 simultaneously
def thread():
    if __name__ == '__main__':
        Thread(target=task2).start()
        Thread(target=task3).start()

task1()
sleep(10)
thread()
