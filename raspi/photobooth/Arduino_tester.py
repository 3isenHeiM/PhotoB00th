#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial


try:
    # Setup the serial port
    arduino = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    arduino.open()
    if arduino.isOpen() : # Returns true if serial port is opened
        print("Serial communication opened to: %s" %arduino.portstr)

except Exception as e :
    print("%s recieved, trying to open the port in 2s" %e)
    arduino.close()
    time.sleep(2)
    arduino.open()
    print("Port was already open, was closed and opened again.")

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
        #time.sleep(1)
        while arduino.inWaiting() > 0:
            # Read a line, decode it as UTF-8 (used by Arduino) and remove \n\r
            out = arduino.readline().decode("utf-8").strip('\n').strip('\r')

        if out != '':
          print "--> " + out
