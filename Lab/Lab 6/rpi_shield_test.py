""" EE 250L Lab 06a
Kristina Kaypaghian and Tina Bao
https://github.com/usc-ee250-fall2018/pcb-design-kristina6/tree/lab06
"""

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration
#CLK = 23
#MISO = 21
#MOSI = 19
#CS = 24
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS,miso=MISO,mosi=MOSI)

# Hardware SPI configuration
# Port and device are 0 becuase we are using SPI0 on your RPi
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Initialize RPi libraries
import RPi.GPIO as GPIO
import time

# Initialize inputs/outputs
LED = 11 # RPi pin 11 for digital output
LIGHT = 0 # ADC channel for analog input
SOUND = 1 # ADC channel for analog input
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(LED, GPIO.OUT) # output LED
GPIO.output(LED,GPIO.LOW) # initialize to no light

# threshold values for sensors
LIGHT_thresh = 200
SOUND_thresh = 200

# intialize counter for sound
n = 0

if __name__ == '__main__':

	while True:

		# blink LED with 500ms delay
		for i in range(5):
			GPIO.output(LED,GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(LED,GPIO.LOW)
			time.sleep(0.5)

		# read light sensor for 5 seconds
		for i in range (50):
			val_LIGHT = mcp.read_adc(LIGHT)
			if val_LIGHT < LIGHT_thresh:
				print(str(val_LIGHT)+" dark")
			else:
				print(str(val_LIGHT)+" bright")
			time.sleep(0.1)
		
		# blink LED with 200ms delay
		for i in range(4):
			GPIO.output(LED,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(LED,GPIO.LOW)
			time.sleep(0.2)

		# read sound sensor for total of 5s
		for i in range(50):
			val_SOUND = mcp.read_adc(SOUND)
			if val_SOUND < SOUND_thresh:
				print(str(val_SOUND)+" loud")  # lab does not say to print loud, but rubric does
				GPIO.output(LED,GPIO.HIGH) # lab says to turn on LED, but rubric does not
				time.sleep(0.1)
				GPIO.output(LED,GPIO.LOW)
			else:
				print(str(val_SOUND)+" quiet")
				GPIO.output(LED,GPIO.LOW)
				time.sleep(0.1)

		# blink LED with 200ms delay
		for i in range(4):
			GPIO.output(LED,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(LED,GPIO.LOW)
			time.sleep(0.2)