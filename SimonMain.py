# A Simon-says style game loop for the Rasberry Pi
# Difficulty sets how long the lights blink for
#   A higher difficutly means shorter lights
# Level starts at 4 (a sequence of 4 blinks) and increases
# 2013-03-30 Kevin Claytor, Michael Simpson and Chris Pecora

import time
import lp_driver	# our controller 
import SiPyVal

def set_diff:
    return 1
    # Right now we'll just implement one difficulty level.

def make_sequence(diff, level):
    seq = []
    for i in xrange(1,level):
        seq.append(random.randint(1,4))
    return seq

def blink_led(LEDPIN,duration):
    GPIO.output(LEDPIN,1)
    sleep(duration)
    GPIO.output(LEDPIN,0);
    return 0

def disp_sequence(diff, seq):
    duration = .5/diff
    for i in seq
        if i == 1:
            blink_led(SiPyVal.RED,duration)
        elif i == 2:
            blink_led(SiPyVal.BLUE,duration)
        elif i == 3:
            blink_led(SiPyVal.GREEN,duration)
        elif i == 4:
            blink_led(SiPyVal.ORANGE,duration)
        else:
            print "Something went wrong..."
    return 0

# Get the user input sequence
def get_user(level):
   # Get the number of keystrokes we need for a level
   pass

# Compare sequences
def seq_compare(seq,useq):
    success = 1
    for i in xrange(0,len(seq)):
        if seq[i] != useq[i]
            success = 0
            break
    return success
    
# Here's the main loop
# First as the user for their difficulty
diff = set_diff()
# Set some constants
success = 1
level = 4

# Now Play a game
while (success):
    seq = make_sequence(diff, level)	# Get the computer sequence	
    disp_sequence(diff, seq)		# Display the sequence
    user = get_user(level)		# Get the user sequence 
    success = seq_compare(seq,user)	# See if they're correct	
    level += 1
    print "Hey, good job!"

print "You Lost! Too Bad, shoulda tried harder!"
