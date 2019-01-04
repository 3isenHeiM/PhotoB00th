#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial

# Setup the serial port
arduino = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

# Try to open port
arduino.isOpen()
print("Serial communication opened to: %s" %ser.portstr)

# Print available commands
print """Enter your commands below. Available commands for the arduino photobooth :
    - Digits from 0 to 9
    - displayOff
    - spotsOn
    - spotsOff
    - spotsDimm
    - S<X>_on to light sport <X>
    - S<X>_off to light out sport <X>
    - animation1
    - animation2
    - animationSpots
    - clear
Insert "exit" to leave the application.
"""

while 1 :
    # get keyboard input
    command = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if command == 'exit':
        arduino.close()
        exit()
    else:
        # send the character to the device
        arduino.write(command + '\r\n')

        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while arduino.inWaiting() > 0:
            # Read a line, decode it as UTF-8 (used by Arduino) and remove \n\r
            out = arduino.readline().decode("utf-8").strip('\n').strip('\r')

        if out != '':
          print "--> " + out
