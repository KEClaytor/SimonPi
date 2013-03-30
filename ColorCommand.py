#!/usr/bin/env python
pipe = open('/dev/input/js0','r')
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
import LpDriver

from time import sleep

def flash(num):
	GPIO.output(num, 1)
	sleep(0.5)
	GPIO.output(num, 0)

while 1:
	key = LpDriver.get_key(pipe)
	if  key == 1:
		flash(25)
	elif key == 2:
		flash(24)
	elif key == 3:
		flash(22)
	elif key == 4:
		flash(17)
