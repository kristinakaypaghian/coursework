import paho.mqtt.client as mqtt
import time
import grovepi

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grove_rgb_lcd

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("tinabao/ledCallback")
    client.message_callback_add("tinabao/ledCallback", led_callback)

    client.subscribe("tinabao/lcdCallback")
    client.message_callback_add("tinabao/lcdCallback", lcd_callback)

#Default message callback. Please use custom callbacks.
#def on_message(client, userdata, msg):
#    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def led_callback(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    message = str(message.payload, "utf-8")
    if message == "LED_ON":
        grovepi.digitalWrite(LED,1)
    elif message == "LED_OFF":
        grovepi.digitalWrite(LED,0)
    #print(message) #for testing purposes

def lcd_callback(client, userdata, message):
    #or should we send all keys from VM, and filter out non a,s,d,w keys in this function?
    #print(str(message.payload, "utf-8")) # TODO: print str or char?
    grove_rgb_lcd.setText_norefresh(str(message.payload, "utf-8"))


if __name__ == '__main__':

    #LED on D4 port
    LED = 4
    grovepi.pinMode(LED,"OUTPUT")

    #ultrasonic on D3 port
    ultrasonic_ranger = 3

    #button on D2 port
    button = 2
    grovepi.pinMode(button,"INPUT")
    #button_test = 1 # for testing purposes

    #clear screen
    grove_rgb_lcd.setText("")

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.led_callback = led_callback
    client.lcd_callback = lcd_callback
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        
        # publish ultrasonic ranger distance
        #dist_int = 0 #for testing purposes w/o grovepi
        dist_int = grovepi.ultrasonicRead(ultrasonic_ranger)
        client.publish("tinabao/ultrasonicCallback", dist_int)

        # check if button is pressed
        #if (button_test == 1): # for testing purposes # replace with line below 
        if (grovepi.digitalRead(button) == 1):
            client.publish("tinabao/button","Button pressed!")

        time.sleep(1)
            

© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
