# LED Server
# 
# This program runs on the Raspberry Pi and accepts requests to turn on and off
# the LED via TCP packets.

import sys
import time
import socket
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../../Software/Python/')

import grovepi

def Main():

    # initialize LED
    LED = 4
    grovepi.pinMode(LED,"OUTPUT")

    host = '192.168.1.83' # Pi IP address
    port = 5001 # port on Pi to receive
    
    s = socket.socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()

    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        #if data = LED_ON, then turn on LED
        if data == "LED_ON":
            grovepi.digitalWrite(LED,1) #turn on LED
            msg = "LED_ON Success"
        #else if data = LED_OFF, then turn off LED
        elif data == "LED_OFF":
            grovepi.digitalWrite(LED,0) #turn off LED
            msg = "LED_OFF Success"
        else:
            msg = "Command not recognized"
        c.send(msg.encode('utf-8'))
    c.close()

if __name__ == '__main__':
    Main()