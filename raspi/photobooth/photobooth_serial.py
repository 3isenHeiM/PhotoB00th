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
    # use global object
    #global arduino

    try:
        # Configure serial comminunication RaspberryPi-Arduino
        arduino = serial.Serial(
            port='/dev/ttyUSB1',
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        # Try to open port
        arduino.isOpen()
        logging.info("Serial communication opened to: %s" %ser.portstr)

    except IOError: # if port is already opened, close it and open it again and print message
      logging.critical("IOError recieved, trying to open the port in 2s")
      arduino.close()
      time.sleep(2)
      arduino.open()
      logging.warning("Port was already open, was closed and opened again.")
