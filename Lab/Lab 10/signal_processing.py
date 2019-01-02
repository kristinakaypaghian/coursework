"""EE 250L Lab 10 Signal Processing
This file is the starter code for the lab assignment.
Kristina Kaypaghian
Tina Bao
https://github.com/usc-ee250-fall2018/signalproc-lab10-kristina10
"""
import requests
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import time

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000

#uncomment these lines to subscribe to real-time published data
ultrasonic_ranger1_topic = "ultrasonic_ranger1/real_data"
ultrasonic_ranger2_topic = "ultrasonic_ranger2/real_data"

#uncomment these lines to subscribe to recorded data being played back in a loop
# ultrasonic_ranger1_topic = "ultrasonic_ranger1/fake_data"
# ultrasonic_ranger2_topic = "ultrasonic_ranger2/fake_data"

# Lists holding the ultrasonic ranger sensor distance readings. Change the 
# value of MAX_LIST_LENGTH depending on how many distance samples you would 
# like to keep at any point in time.

# play with different buffer sizes
MAX_LIST_LENGTH = 10 #10 max and 3 comparison worked best
ranger1_dist = [0]*MAX_LIST_LENGTH # TODO: if you fill it up with zeros first
avg1 = [0]*MAX_LIST_LENGTH
diff1 = [0]*MAX_LIST_LENGTH
ranger2_dist = [0]*MAX_LIST_LENGTH
avg2 = [0]*MAX_LIST_LENGTH
diff2 = [0]*MAX_LIST_LENGTH
state = 0 # initialize state machine
comparison = 4 #2 # TODO: comparison value for final buffer value to determine movement direction
waitCounter = 0
POSTstr = "" # initialize string for POST

def ranger1_callback(client, userdata, msg):
    global ranger1_dist
    ranger1_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
    global ranger2_dist
    ranger2_dist.append(int(msg.payload))
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(ultrasonic_ranger1_topic)
    client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
    client.subscribe(ultrasonic_ranger2_topic)
    client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

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

    # This header sets the HTTP request's mimetype to `application/json`. This
    # means the payload of the HTTP message will be formatted as a json ojbect
    hdr = {
        'Content-Type': 'application/json',
        'Authorization': None #not using HTTP secure
    }

    while True:
        
        dist_left_list = ranger1_dist[-1:]
        dist_left = dist_left_list[0]
        dist_right_list = ranger2_dist[-1:]
        dist_right = dist_right_list[0]

        # Calculate avg buffer and slope
        # avg buffer: average the sample buffer into avg buffer
        # add up all values in sample buffer then divide by length of sample buffer
        total1 = 0
        total2 = 0
        index = 0
        while (index < MAX_LIST_LENGTH):
            total1 = ranger1_dist[index]+total1
            total2 = ranger2_dist[index]+total2
            index = index + 1
        # append value into sample buffer   
        average1 = total1/MAX_LIST_LENGTH
        average2 = total2/MAX_LIST_LENGTH
        avg1.append(average1)
        avg2.append(average2)
        avg1 = avg1[-MAX_LIST_LENGTH:]
        avg2 = avg2[-MAX_LIST_LENGTH:]

        waitCounter = waitCounter+1
        # wait for buffer to fill up with real values (not initialized 0's) and
        # wait for average buffer to fill up with values (that don't take into account initialized 0's)
        if ( waitCounter > (MAX_LIST_LENGTH*2) ) :
            # calculate difference in avg buffer
            # use for loop to iterate over pairs of elements in avg buffer
            # take the difference between two pairs
            # store value into new list of the
            x = 0
            while (x < (MAX_LIST_LENGTH-1)):
                difference1 = avg1[x+1]-avg1[x]
                difference2 = avg2[x+1]-avg2[x]
                diff1.append(difference1)
                diff2.append(difference2)
                diff1 = diff1[-MAX_LIST_LENGTH:]
                diff2 = diff2[-MAX_LIST_LENGTH:]
                x = x+1
                pass
            # average the differences into final buffer
            avgdiff1 = sum(diff1) / len(diff1)
            #print("avgdiff1: " + str(avgdiff1))
            avgdiff2 = sum(diff2) / len(diff2)
            #print("avgdiff2: " + str(avgdiff2))





            # state machine
            # intialize state to 0 (out of range of both sensors)
            # There are two paths for this state machine
            # One path (0 -> 1 -> 2 -> 3 -> 0) moving right
            # One path (0 -> -1 -> -2 -> -3 -> 0) moving left
            # To determine which path, first detect if person is in front of a sensor and which sensor

            # moving right
            if (state == 0): # out of rangers
                print("Out of range")
                POSTstr = "Out of range"
                if (avgdiff1 < -comparison): # entering ranger1
                    state = 1
                    POSTstr = "Moving Right"
                elif (avgdiff2 < -comparison): # entering ranger2
                    state = -1
                    POSTstr = "Moving Left"
            elif (state == 1): # in front of ranger1
                if ( (avgdiff1 > -comparison) and (avgdiff1 < comparison) ):
                    POSTstr ="Still - Left"
                elif (avgdiff1 > comparison): # leaving ranger1
                    state = 2
                else:
                    POSTstr="Moving Right"
            elif (state == 2): # in between rangers
                if (avgdiff2 < -comparison): # entering ranger2
                    state = 3
                    POSTstr="Moving Right"
            elif (state == 3): # in front of ranger2 
                if ( (avgdiff2 > -comparison) and (avgdiff2 < comparison) ):
                    POSTstr = "Still - Right"
                elif (avgdiff2 > comparison): # leaving ranger2
                    state = 0
                else:
                    POSTstr="Moving Right"
                    


            # moving left
            # state 0 to state -1 included above
            elif (state == -1): # in front of ranger 2
                #print(state)
                if ( (avgdiff2 > -comparison) and (avgdiff2 < comparison) ):
                    POSTstr="Still - Right"
                elif (avgdiff2 > comparison): # leaving ranger2
                    state = -2
                    POSTstr="Moving Left"
                else:
                    POSTstr="Moving Left"
            elif (state == -2): # in between rangers
                if (avgdiff1 < -comparison): # entering ranger1
                    state = -3
                    POSTstr="Moving Left"
            elif (state == -3): # in front of ranger 1
                if ( (avgdiff1 > -comparison) and (avgdiff1 < comparison) ):
                    POSTstr="Still - Left"
                elif (avgdiff1 > comparison): # leaving ranger1
                    state = 0
                else:
                    POSTstr="Moving Left"

            print(POSTstr)

            
            # prepare POST payload
            payload = {
                'time': str(datetime.now()),
                'event': POSTstr
            }
            

            # Send an HTTP POST message and block until a response is given.
            # TODO: Note: requests() is NOT the same thing as request() under the flask 
            # library
            response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr, data = json.dumps(payload))

            # Print the json object from the HTTP response 
            print(response.json())


        time.sleep(0.2)