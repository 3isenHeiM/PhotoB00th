#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import traceback
import logging
from logging import handlers
import argparse
import gzip
import gphoto2 as gp
import serial

#####################################
# FUNCTIONS
#####################################
# Manage Ctrl+C gracefully
def signal_handler_quit(signal, frame):
    logging.info("Shutting down pyBus...")
    core.shutdown()
    logging.critical("pyBus shutdown.\n")
    sys.exit(0)



#################################
# LOGGING
#################################

# Convert verbose count in loggin level for the loggin module
def logging_level(verbosity):
    levels = [
        logging.CRITICAL,   # 50
        logging.ERROR,      # 40
        logging.WARNING,    # 30
        logging.INFO,       # 20
        logging.DEBUG       # 10
    ]
    return levels[max(min(len(levels) - 1, verbosity), 0)]

def configureLogging(numeric_level,logfile):
    ## VARIABLES
    format_entry = '%(asctime)s.%(msecs)03d | %(module)-17s [%(levelname)-8s] %(message)s'
    format_date = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format_entry, format_date)
    log_lvl = logging_level(numeric_level)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Logging to sys.stderr
    consolehandler = logging.StreamHandler(sys.stdout)
    consolehandler.setLevel(log_lvl)
    consolehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)

    # Logging to file is provided
    if logfile :
        # Put the right filename to core.LOGFILE
        core.LOGFILE = logfile
        # Use rotating files : 1 per day, and all are kept (no rotation thus)
        filehandler = handlers.TimedRotatingFileHandler(logfile, when='d', interval=1, backupCount=0)
        filehandler.suffix = "%Y-%m-%d"
        # We can set here different log formats for the stderr output !
        filehandler.setLevel(0)
        # use the same format as the file
        filehandler.setFormatter(formatter)
        # add the handler to the root logger
        logger.addHandler(filehandler)

    logging.info("Logging level set to %s", logging_level(numeric_level))

#################################
# Program options
#################################
def createParser():
    parser = argparse.ArgumentParser(epilog="If you have any questions : https://github.com/3isenHeiM/Photobooth",\
                                     description="This is %(prog)s, the programm to turn a RapsberryPi and an Arduino Uno into a photobooth")
    parser.add_argument('-v', '--verbose', action='count', default=0,\
                        help='Increases verbosity of logging (up to -vvvv).')
    parser.add_argument('-o', '--output_file', action='store', default='',\
                      help='Path/Name of log file (log level of 0). If no file specified, output only to std.out')
    return parser

def restart():
    args = sys.argv[:]
    logging.info('Re-spawning %s' % ' '.join(args))

    args.insert(0, sys.executable)

    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)


def initSerial():
# Configure serial comminunication RaspberryPi-Arduino
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()



#####################################
# MAIN
#####################################
parser       = createParser()
results      = parser.parse_args()
loglevel     = results.verbose
core.DEVPATH = results.device
_startup_cwd = os.getcwd()

# Manage Ctrl+C
signal.signal(signal.SIGINT, signal_handler_quit)

configureLogging(loglevel, results.output_file)

try:
    logging.critical("pyBus started !")
    core.initialize()
    core.run()
except Exception:
    logging.error("Caught unexpected exception:")
    logging.error(traceback.format_exc())
    logging.info("Going to sleep 2 seconds and restart")
    time.sleep(2)
    restart()

sys.exit(0)


print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(input + '\r\n')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
          print ">>" + out
```

## Capture and download using python

From python-gphoto2 [examples](https://github.com/jim-easterbrook/python-gphoto2/blob/master/examples/capture-image.py).
Two functions are used : 
* `gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE)`  
to trigger the shot
* `gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)`  
to download the image

```

from __future__ import print_function

import logging
import os
import subprocess
import sys

import gphoto2 as gp

def main():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join('/tmp', file_path.name)
    print('Copying image to', target)
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    subprocess.call(['xdg-open', target]) # To open the image in the preferred editor
    gp.check_result(gp.gp_camera_exit(camera))
    return 0

if __name__ == "__main__":
sys.exit(main())
```
