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
import RPi.GPIO as GPIO
import threading
import SimpleHTTPServer
import SocketServer


#####################################
# FUNCTIONS
#####################################
# Manage Ctrl+C gracefully
def signal_handler_quit(signal, frame):
    logging.info("Shutting down requested")
    GPIO.cleanup()
    webserver.shutdown()
    logging.debug("Cleaned up GPIO's")
    logging.critical("Photob00th shutdown.\n")
    sys.exit(0)

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    # Logs in a separated file
    buffer = 1
    logfile = "webserver.log"
    log_file = open(logfile, 'w', buffer)
    logging.info('Web Server logs are in %s' %logfile )
    def log_message(self, format, *args):
        self.log_file.write("%s - [%s] : %s\n" %(
            self.client_address[0],self.log_date_time_string(),format%args))


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
    format_entry = '%(asctime)s.%(msecs)03d [%(levelname)-8s] %(message)s'
    format_date = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format_entry, format_date)
    log_lvl = logging_level(numeric_level)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Logging to sys.stdout
    consolehandler = logging.StreamHandler(sys.stdout)
    consolehandler.setLevel(log_lvl)
    consolehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)

    # Logging to file is provided
    if logfile :
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
                      help='Path/Name of log file (log level of 0). If no file specified, output only to stdout')
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
_startup_cwd = os.getcwd()

# Manage Ctrl+C
signal.signal(signal.SIGINT, signal_handler_quit)

configureLogging(loglevel, results.output_file)

try:
    logging.critical("Photob00th started !")
    # Launch the webserver
    PORT = 8000
    webserver = SocketServer.TCPServer(("", PORT), CustomHTTPRequestHandler)
    thread = threading.Thread(target = webserver.serve_forever)
    thread.daemon = True
    thread.start()
    logging.info('Starting webserver on port %d', PORT )
    # Init the serial port
    # initSerial()
    logging.info('Starting serial communication' )

    # Main business

except Exception:
    logging.error("Caught unexpected exception:")
    logging.error(traceback.format_exc())
    logging.info("Going to sleep 2 seconds and restart")
    time.sleep(2)
    restart()

sys.exit(0)




# ## Capture and download using python
#
# From python-gphoto2 [examples](https://github.com/jim-easterbrook/python-gphoto2/blob/master/examples/capture-image.py).
# Two functions are used :
# * `gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE)`
# to trigger the shot
# * `gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)`
# to download the image
#
# ```
#
# from __future__ import print_function
#
# import logging
# import os
# import subprocess
# import sys
#
# import gphoto2 as gp
#
# def main():
#     gp.check_result(gp.use_python_logging())
#     camera = gp.check_result(gp.gp_camera_new())
#     gp.check_result(gp.gp_camera_init(camera))
#     print('Capturing image')
#     file_path = gp.check_result(gp.gp_camera_capture(
#         camera, gp.GP_CAPTURE_IMAGE))
#     print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
#     target = os.path.join('/tmp', file_path.name)
#     print('Copying image to', target)
#     camera_file = gp.check_result(gp.gp_camera_file_get(
#             camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
#     gp.check_result(gp.gp_file_save(camera_file, target))
#     subprocess.call(['xdg-open', target]) # To open the image in the preferred editor
#     gp.check_result(gp.gp_camera_exit(camera))
#     return 0
#
# if __name__ == "__main__":
# sys.exit(main())
# ```
