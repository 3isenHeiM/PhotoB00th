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
    logging.debug("Cleaned up GPIO's")

    webserver.shutdown()
    logging.debug("Webserver shutdown")

    gp.check_result(gp.gp_camera_exit(camera))
    logging.info("Releasing camera")

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

# Init the camera, opens the connections and set the target to the SD card
def initCamera(camera, context):
    # Detects the camera
    while True:
        error = gp.gp_camera_init(camera, context)
        if error >= gp.GP_OK:
            # Camera detected, get the model
            logging.info("Camera detected")
            break
        if error != gp.GP_ERROR_MODEL_NOT_FOUND:
            # some other error we can't handle here
            raise gp.GPhoto2Error(error)
        else :
            # no camera, try again in 2 seconds
            logging.error("Camera not found, trying again in 2s...")
            time.sleep(2)

    # continue with rest of program

    # Get configuration tree
    cameraConfig = gp.check_result(gp.gp_camera_get_config(camera))
    # Get Camera model
    cameraNameWidget = gp.check_result(
                gp.gp_widget_get_child_by_name(cameraConfig, 'model'))
    cameraName = ""
    cameraName = gp.check_result(
                    gp.gp_widget_get_value(cameraNameWidget))#, cameraName))
    logging.info("Camera model : %s" %cameraName)

    # Find the capture target config item
    captureTarget = gp.check_result(
        gp.gp_widget_get_child_by_name(cameraConfig, 'capturetarget'))

    value = 1 # 0 is for internal memory, 1 is for SD card
    # Check value in range
    count = gp.check_result(gp.gp_widget_count_choices(captureTarget))
    if value < 0 or value >= count:
        logging.error('Parameter out of range')
        return 1
    # set value
    value = gp.check_result(gp.gp_widget_get_choice(captureTarget, value))
    gp.check_result(gp.gp_widget_set_value(captureTarget, value))
    # set config
    gp.check_result(gp.gp_camera_set_config(camera, cameraConfig))

    return camera

# Captures an image, take the current time and save in into the inputted folder.
# Input : GPhoto camera object, Folder where to save the pictures
# Output : name of the latest picture taken
def takePhoto(camera, pictureFolder):
    logging.info('Capturing image...')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    logging.debug('Picture path: {0}/{1}'.format(file_path.folder, file_path.name))
    # Get the name of the picture just taken
    pictureFile = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))

    # Build a timestamp to name the picture
    now = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    newPictureFile = os.path.join(pictureFolder, timestamp)

    gp.check_result(gp.gp_file_save(pictureFile, newPictureFile))
    logging.info('New picture : ', newPictureFile)

    return timestamp


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
                        filename='debug.log')

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
    #logging.getLogger('gphoto2').setLevel(logging.WARNING)

    return logging

#################################
# Program options
#################################
def createParser():
    parser = argparse.ArgumentParser(epilog="If you have any questions : https://github.com/3isenHeiM/Photobooth",\
                                     description="This is %(prog)s, the programm to turn a RapsberryPi and an Arduino Uno into a photobooth")
    parser.add_argument('-v', '--verbose', action='count', default=3,\
                        help='Increases verbosity of logging (up to -vvvv).')
    parser.add_argument('-o', '--output_file', action='store', default='',\
                      help='Path/Name of log file (log level of 0). If no file specified, output only to stdout')
    parser.add_argument('-c', '--console', action='store_true',\
                      help='Enable logging output on STDOUT')
    parser.add_argument('-t', '--test', action='store_true', \
                        help='Run the program interactively to simulate Arduino communication. User will have to provide the commands to take pictures, etc...')
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
testMode     = results.test
_startup_cwd = os.getcwd()
context      = gp.Context()
camera       = gp.Camera()
pictureFolder = os.getcwd() + "/images/jpg"


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

    initCamera(camera, context)

    if camera == None :
        logging.error("Error initializing camera")
        sys.exit(2)
    else :
        logging.info('Camera initialized')

    if not testMode :
        # Init the serial port
        # initSerial()
        logging.info('Starting serial communication' )
    else :
        logging.info('Starting program in interactive mode')
        input()
    # Main business here

except Exception:
    logging.error("Caught unexpected exception:")
    logging.error(traceback.format_exc())
    logging.info("Going to sleep 2 seconds and restart")
    #time.sleep(2)
    #restart()

sys.exit(0)
