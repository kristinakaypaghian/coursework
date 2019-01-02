""" EE 250L Lab 02: GrovePi Sensors
Kristina Kaypaghian
Tina Bao
https://github.com/usc-ee250-fall2018/GrovePi-kristina/tree/lab02/ee250/lab02
Each team member should submit a copy of the team's code.
"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages
The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""


#### import libraries

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import time
from math import isnan
from grovepi import *
import grove_rgb_lcd
from grove_dht_pro_filter import *

#### set ports

# rotary input on analog port A0
rotary = 0

# ultrasonic on digital port D3
ultrasonic_ranger = 3

# humidity and temperature sensor DHT on digital port D4
dht_pin = 4

#### initialize variables (in case of NAN first reading)
humidity_string = " "
temp_string = " "

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""
if __name__ == '__main__':

    #clear screen
    grove_rgb_lcd.setText("")

    while True:
        #So we do not poll the sensors too quickly which may introduce noise,
        #sleep for a reasonable time of 200ms between each iteration.
        time.sleep(1.1) #1.1 works

        #read rotary input
        rotary_float = analogRead(rotary)
        map_float = (rotary_float*517)/1023
        map_int = int(map_float)
        dist_thresh_int = map_int
        dist_thresh_string = str(map_int)

        #read ultrasonic ranger, convert int to string, display on LCD
        dist_int = ultrasonicRead(ultrasonic_ranger)
        dist_string = str(dist_int)

        #read humidity
        [temp,humidity] = dht(dht_pin,0) # instantiate a dht class with the appropriate pin
        # TODO: if isnano is true, just ignore don't print
        if isnan(temp) is False and isnan(humidity) is False:
            temp_int = int(temp)
            humidity_int = int(humidity)
            temp_string = str(temp_int)
            humidity_string = str(humidity_int)

        #display

        #format strings
        if len(dist_thresh_string) == 1:
            dist_thresh_string += "  "
        elif len(dist_thresh_string) == 2:
            dist_thresh_string += " "

        #compare ultrasonic ranger with threshold
        if isnan(temp) is False and isnan(humidity) is False:
            if dist_int < dist_thresh_int :
                grove_rgb_lcd.setText_norefresh(dist_thresh_string+" OBJ PRESENT"+"\n"+dist_string+"cm "+ humidity_string +"% " + temp_string + "C")
            else :   
                grove_rgb_lcd.setText_norefresh(dist_thresh_string+"            \n"+dist_string+"cm "+ humidity_string +"% " + temp_string + "C")



