#Ultrasonic Sensor Server
#
# This code runs on your VM and receives a stream of packets holding ultrasonic
# sensor data and prints it to stdout. Use a UDP socket here.

import socket

def Main():
    host = '10.0.2.15' # the VM IP address
    port = 9000 # listening on VM port from the host # should match guest port on port forwarding

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("Ultrasonic server started")
    while True:
        data, addr = s.recvfrom(1024) # size
        data = data.decode('utf-8')
        print("VM: " + data + " cm")
    c.close()
    

if __name__ == '__main__':
    Main()