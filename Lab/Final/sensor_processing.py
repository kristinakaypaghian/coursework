"""EE 250L Lab 11 Final Project
sensor_processing.py: Sensor data processing.
Kristina Kaypaghian
Tina Bao
https://github.com/usc-ee250-fall2018/finalproj-riot-kristtinafinal
"""

import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000

# topic name
light_topic = "kaypaghi/light"
flag = 10 # initialize

# callback function
def light_callback(client, userdata, msg):
    # This header sets the HTTP request's mimetype to `application/json`. This
    # means the payload of the HTTP message will be formatted as a json ojbect
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }
    
    global flag

    if((flag==0 or flag ==10) and (int(msg.payload) < 300)):
        payload = {
            'time': str(datetime.now()),
            'event': "LIGHTS_OFF",
            'room': "vhe_205"
        }
        flag = 1
    elif((flag == 1 or flag == 10) and (int(msg.payload) > 300)):
        payload = {
            'time': str(datetime.now()),
            'event': "LIGHTS_ON",
            'room': "vhe_205"
        }
        flag = 0
    

    response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr, data = json.dumps(payload))

    # Print the json object from the HTTP response
    print(response.json())

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(light_topic)
    client.message_callback_add(light_topic, light_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_hostname, broker_port, 60)
    client.loop_start()

    while True:
        
        time.sleep(0.2)