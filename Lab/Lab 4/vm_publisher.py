"""
Kristina Kaypaghian
Tina Bao
https://github.com/usc-ee250-fall2018/grovepi-lab04-kristina4/tree/lab04/ee250/lab04
"""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard

global msg
global kSend
msg = ""
kSend = ""
kOld = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_press(key):
    global msg
    global kSend

    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        #send "w" character to rpi
        kSend = k
    elif k == 'a':
        # send "a" character to rpi
        kSend = k
        #send "LED_ON"
        msg = "LED_ON"
    elif k == 's':
        # send "s" character to rpi
        kSend = k
    elif k == 'd':
        # send "d" character to rpi
        kSend = k
        # send "LED_OFF"
        msg = "LED_OFF"
    #TODO: using kSend to avoid sending other characters 



if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:

    	#TODO: use select ^= 1 to move between publishing different things?
        client.publish("tinabao/ledCallback", msg)
        if kSend != kOld:
        	client.publish("tinabao/lcdCallback", kSend)
        #print(k)
        kOld = kSend
        time.sleep(1)