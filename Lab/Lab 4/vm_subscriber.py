"""EE 250L Lab 04 Starter Code
Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("tinabao/ultrasonicCallback")
    client.message_callback_add("tinabao/ultrasonicCallback", ultrasonic_callback)

    client.subscribe("tinabao/button")
    client.message_callback_add("tinabao/button", button_callback)
    
def ultrasonic_callback(client, userdata, dist):
    print("VM: " + str(dist.payload, "utf-8") + " cm")

def button_callback(client, userdata, message):
    print(str(message.payload, "utf-8"))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)