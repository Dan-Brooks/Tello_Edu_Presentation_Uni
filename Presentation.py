import time
from time import sleep

import cv2
import socket
from threading import Thread
import numpy as np

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_VIDEO_PORT = 11111
bufferSize = 1024

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = (TELLO_IP, TELLO_PORT)

# Send command to Tello
def send_command(command):
    sock.sendto(command.encode('utf-8'), tello_address)
    msg = sock.recvfrom(bufferSize)
    return msg


msg = send_command("command")
print(msg)

def Task1():
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

def Task2():
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

def Task3():
    msg = send_command("streamon")
    print(msg)

    cap = cv2.VideoCapture(f'udp://{TELLO_IP}:{TELLO_VIDEO_PORT}')


    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('Tello Video Stream', frame)

            cv2.imshow('img1', frame)  # display the captured image
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

def thread():
    if __name__ == '__main__':
        Thread(target=Task2).start()
        Thread(target=Task3).start()

Task1()
sleep(10)
thread()
