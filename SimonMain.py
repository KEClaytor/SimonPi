#!/usr/bin/env python
# A Simon-says style game loop for the Rasberry Pi
# Difficulty sets how long the lights blink for
#   A higher difficutly means shorter lights
# Level starts at 4 (a sequence of 4 blinks) and increases
# 2013-03-30 Kevin Claytor, Michael Simpson and Chris Pecora

import RPi.GPIO as GPIO
import LpDriver
import SiPiVal as SPV
from time import sleep

# Open the path to the controller data
pipe = open('/dev/input/js0','r')
# Initalize Pi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPV.RED, GPIO.OUT)
GPIO.setup(SPV.BLUE, GPIO.OUT)
GPIO.setup(SPV.GREEN, GPIO.OUT)
GPIO.setup(SPV.ORANGE, GPIO.OUT)

# LED helper functions
def onoff_led(PINS,state):
    for PIN in PINS:
        GPIO.output(PIN,state)
    return 0

def blink_led(LEDPIN,duration):
    onoff_led(LEDPIN,1)
    sleep(duration)
    onoff_led(LEDPIN,0)
    return 0

# Get game mode, TRUE = append to sequence = up arrow
#                FALSE = new sequence = down arrow
def get_mode():
    print "Select game mode:"
    print "   ^  = Append"
    print "   \/ = New (Challenge mode)"
    onoff_led(SPV.UPARROW,1)
    mode = True
    while 1:
        key = LpDriver.get_key(pipe)
        if key == SPV.SELECT:
            if mode:
                onoff_led(SPV.UPARROW,0)
                onoff_led(SPV.DNARROW,1)
            else:
                onoff_led(SPV.DNARROW,0)
                onoff_led(SPV.UPARROW,1)
            mode = not mode
        elif key == SPV.START:
            break
    return mode
        
def get_diff():
    print "Select your difficutly:"
    print " 1 = Easy"
    print " 2 = Hard"
    print " 3 = Harder"
    print " 4 = Hardest"
    diff = 1
    onoff_led([SPV.LEDUP],1)
    while 1:
        key = LpDriver.get_key(pipe)
        if key == SPV.SELECT:
            if diff == 1:
                onoff_led([SPV.LEDRT],1)
                diff += 1
            elif diff == 2:
                onoff_led([SPV.LEDDN],1)
                diff += 1
            elif diff == 3:
                onoff_led([SPV.LEDLT],1)
                diff += 1
            else:
                onoff_led([SPV.LEDRT],0)
                onoff_led([SPV.LEDDN],0)
                onoff_led([SPV.LEDLT],0)
                diff = 1
        elif key == SPV.START:
            break
    return diff

# Generates a sequence of LED values level long
def make_sequence(diff, level):
    seq = []
    for i in xrange(1,level):
        seq.append(SPV.LEDALL[random.randint(0,3)])
    return seq

def disp_sequence(diff, seq):
    duration = .5/diff
    for LED in seq:
        blink_led(LED,duration)
    return 0

# Get the user input sequence
def get_user(level):
    user = []
    # Get the number of keystrokes we need for a level
    for i in xrange(1,level):
        key = LpDriver.get_key(pipe)
        user.append(key)
        # Blink the LED as user feedback
        if key == SPV.LPUP:
            blink_led([SPV.LEDUP],.5)
        elif key == SPV.LPDN:
            blink_led([SPV.LEDDN],.5)
        elif key == SPV.LPLT:
            blink_led([SPV.LEDLT],.5)
        elif key == SPV.LPRT:
            blink_led([SPV.LEDRT],.5)
        elif key == SPV.START:
            # Little easter egg, the player looses in this case though
            blink_led(SPV.LEDALL,.5)
    return user

# Compare sequences
def seq_compare(seq,useq):
    success = True
    for i in xrange(0,len(seq)):
        led_dir = seq[i]
        user_dir = useq[i]
        if (led_dir == SPV.LEDUP):
            if (user_dir != SPV.LPUP):
                success = False
                break
        elif (led_dir == SPV.LEDDN):
            if (user_dir != SPV.LPDN):
                success = False
                break
        elif (led_dir == SPV.LEDLT):
            if (user_dir != SPV.LPLT):
                success = False
                break
        elif (led_dir == SPV.LEDRT):
            if (user_dir != SPV.LPRT):
                success = False
                break
        return success
    
# ==============================
# ======= MAIN GAME LOOP =======
# ==============================

# Select the game mode
mode = get_mode()
# First as the user for their difficulty
diff = get_diff()
# Set some constants
success = True
level = 3

# Now Play a game
seq = make_sequence(diff, level)	# Get the computer sequence	
while success:
    if mode:
        seq.append(SPV.LEDALL[random.randint(0,3)])
    else:
        seq = make_sequence(diff, level)
    disp_sequence(diff, seq)		# Display the sequence
    user = get_user(level)		# Get the user sequence 
    success = seq_compare(seq,user)	# See if they're correct	
    level += 1
    print "Hey, good job! Level" + repr(level) + " passed!"

print "You Lost! Too Bad, shoulda tried harder!"
