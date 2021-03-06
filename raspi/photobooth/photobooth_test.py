#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, os.path
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
import threading
import SimpleHTTPServer
import SocketServer

# Project-related imports
import photobooth_serial as pb_serial
import photobooth_camera as pb_camera
import photobooth_image as pb_image

#####################################
# FUNCTIONS
#####################################
# Manage Ctrl+C gracefully
def signal_handler_quit(signal, frame):
    logging.info("Shutting down requested")

    webserver.shutdown()
    logging.debug("Webserver shutdown")

    gp.check_result(gp.gp_camera_exit(camera))
    logging.info("Releasing camera")

    logging.critical("Photob00th shutdown.\n")
    sys.exit(0)


# Class to create the WebServer and to log the requests in a separate file
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

def configureLogging(numeric_level, logfile, console):
    ## VARIABLES
    format_entry = '%(asctime)s.%(msecs)03d | %(module)-10s [%(levelname)-8s] %(message)s'
    format_date = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format_entry, format_date)
    log_lvl = logging_level(numeric_level)

    # Configure root logger to a file
    logging.root.handlers = []
    logging.basicConfig(format='%(asctime)s.%(msecs)03d | %(module)-10s [%(levelname)-8s] %(message)s',\
                        level=logging.DEBUG ,\
                        filename='test_debug.log')

    if console :
        # Logging to sys.stderr
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(log_lvl)
        consolehandler.setFormatter(formatter)
        logging.getLogger("").addHandler(consolehandler)

    # Logging to file is provided
    if logfile :
        # Use rotating files : 1 per day, and all are kept (no rotation thus)
        filehandler = handlers.TimedRotatingFileHandler(logfile, when='d', interval=1, backupCount=0)
        filehandler.suffix = "%Y-%m-%d"
        # We can set here different log formats for the stderr output !
        filehandler.setLevel(logging.DEBUG)
        # use the same format as the file
        filehandler.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger("").addHandler(filehandler)

    logging.info("Logging level set to %s", logging_level(numeric_level))

    # Have Gphot2 lgos in python logging module
    gp.use_python_logging()
    logging.getLogger('gphoto2').setLevel(logging.DEBUG)

    return logging

#################################
# Program options
#################################
def createParser():
    parser = argparse.ArgumentParser(epilog="If you have any questions : https://github.com/3isenHeiM/Photobooth",\
                                     description="This is %(prog)s, the program to test the good processing of the commands sent by the arduino")
    parser.add_argument('-v', '--verbose', action='count', default=3,\
                        help='Increases verbosity of logging (up to -vvvv).')
    parser.add_argument('-o', '--output_file', action='store', default='',\
                      help='Path/Name of log file (log level of 0). If no file specified, output only to stdout')
    parser.add_argument('-t', '--test', action='store_true', \
                        help='Do not try to control the camera')
    parser.add_argument('-c', '--console', action='store_true',\
                      help='Enable logging output on STDOUT')
    parser.add_argument('-n', '--no-filter', action='store_false', dest="noFilter", \
                      help='Disables the instagram-like filter when processing the images.')
    return parser

def restart():
    args = sys.argv[:]
    logging.info('Re-spawning %s' % ' '.join(args))

    args.insert(0, sys.executable)
    time.sleep(1)
    os.chdir(_startup_cwd)
    os.execv(sys.executable, args)

#####################################
# MAIN
#####################################
parser       = createParser()
results      = parser.parse_args()
testMode     = results.test
_startup_cwd = os.getcwd()
pictureFolder = "images/jpg"
batt_lvl     = 25

pb_image.enableFilter = results.noFilter

# Init the Gphoto2 objects
context      = gp.Context()
camera       = gp.Camera()

log = configureLogging(results.verbose, results.output_file, results.console)

# Manage Ctrl+C
signal.signal(signal.SIGINT, signal_handler_quit)

try:
    logging.info("Photob00th started !")

    # Launch the webserver
    PORT = 8000
    webserver = SocketServer.TCPServer(("", PORT), CustomHTTPRequestHandler)
    thread = threading.Thread(target = webserver.serve_forever)
    thread.daemon = True
    thread.start()
    logging.info('Starting webserver on port %d', PORT )

    if not testMode :
        # Init the camera
        pb_camera.initCamera(camera, context)

        if camera == None :
            logging.error("Error initializing camera")
            sys.exit(2)
        else :
            logging.info('Camera initialized')

    else :
        logging.info('Starting program in interactive mode')

    # Get the image count
    pb_image.getImageCount()
    logging.info("Image count : %d" %pb_image.count)

    # Available functions :
    # - takePhoto

    input=1
    while True :
        # Get keyboard input
        command = raw_input("Enter your command : ")

        logging.debug("Command received : %s" %command)

        if command == 'takePhoto':
            pictureName = pb_camera.takePhoto(camera, pictureFolder)

            logging.info("Triggered postprocessing script")

            pb_image.postProcess(pictureName)

        elif command == "ready" :
            # Do nothing
            logging.info("Ready")

        else :
            logging.info("Unknown command")


except Exception:
    logging.error("Caught unexpected exception:")
    logging.error(traceback.format_exc())
    logging.warning("Going to sleep 2 seconds and restart")
    time.sleep(2)
    # Cancelled the restart for testing purposes
    #restart()

sys.exit(0)
