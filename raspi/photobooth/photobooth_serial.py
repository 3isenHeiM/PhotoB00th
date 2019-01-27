#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import traceback
import logging
from logging import handlers
import serial
import threading


def initSerial(arduino):
    try:
        # Configure serial communication RaspberryPi-Arduino
        arduino = serial.Serial(
            #port='/dev/ttyUSB1',
            port='/dev/ttyACM0',
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        # Try to open port
        arduino.open()
        if arduino.isOpen() : # Returns true if serial port is opened
            logging.info("Serial communication opened to: %s" %arduino.portstr)
        else :
            raise IOError

    except IOError: # if port is already opened, close it and open it again and print message
      logging.critical("IOError recieved, trying to open the port in 2s")
      arduino.close()
      time.sleep(2)
      arduino.open()
      logging.warning("Port was already open, was closed and opened again.")


    return arduino
