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



while 1 :
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        while arduino.inWaiting() > 0:
            # Read a line, decode it as UTF-8 (used by Arduino) and remove \n\r
            out = arduino.readline().decode("utf-8").strip('\n').strip('\r')

        if out != '':
          print "--> " + out
