# Ultrasonic Sensor Client
# 
# This code runs on the Raspberry Pi. It should sit in a loop which reads from
# the Grove Ultrasonic Ranger and sends the reading to the Ultrasonic Sensor 
# Server running on your VM via UDP packets. 

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are able to successfully `import grovepi`
sys.path.append('../../../Software/Python/')

import time
import grovepi
import socket

#ultrasonic on D3 port
ultrasonic_ranger = 3

def Main():
    host = '192.168.1.83' # the Pi IP address
    port = 5001   #the port that Pi is using to send out data

    server_addr = '192.168.1.56' # the mac IP address

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    
    while True:
        dist_int = grovepi.ultrasonicRead(ultrasonic_ranger)
        dist_str = str(dist_int)
        dst_port = 8050 #should match host Port in port forwarding
        message = dist_str
        print("RPI: " + message + " cm")
        server = (server_addr, int(dst_port))
        s.sendto(message.encode('utf-8'), server)
        #time.sleep(.2)
    s.close()


if __name__ == '__main__':
    Main()