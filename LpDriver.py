#!/usr/bin/env python
#pipe = open('/dev/input/js0','r')

import sys
def get_key(pipe):
    key = False
    action = []
    spacing = 0

    LEFT=11
    RIGHT=12
    UP=13
    DOWN=14

    KEY={"01000100": 1,
         "01000101": 2,
         "01000102": 3,
         "01000103": 4,
         "01000104": 5,
         "01000105": 6,
         "01000106": 7,
         "01000107": 8,
         "01000108": 9,
         "01000109": 10,
         "01800200": 11,
         "FF7F0200": 12,
         "01800201": 13,
         "FF7F0201": 14
         }

    while not key:
        for character in pipe.read(1):
            action += [character]
            if len(action) == 16:
                a = []
                for byte in action:
                    a.append('%02X' % ord(byte))
                    spacing += 1
                    if spacing == 16:
                        try:
                            key = KEY["".join(a[4:8])]
                        except:
                            key = "".join(a[4:8])
                        spacing = 0
                        sys.stdout.flush()
                        action = []
                        return key

