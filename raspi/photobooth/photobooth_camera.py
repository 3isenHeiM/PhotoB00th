#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import traceback
import logging
import datetime
from logging import handlers
import gzip
import gphoto2 as gp


# Init the camera, opens the connections and set the target to the SD card
def initCamera(camera, context):
    # Globals to take the modifs into account in other parts
    # Needed to modify global copy of camera and context variables
    #global camera, context

    # Detects the camera X times
    tryouts = 10
    for x in range(1, tryouts+1):
        error = gp.gp_camera_init(camera, context)
        if error >= gp.GP_OK:
            # Camera detected, get the model
            logging.info("Camera detected")
            break
        elif error == gp.GP_ERROR_MODEL_NOT_FOUND:
            # no camera, try again in 2 seconds
            logging.error("Camera not found ("+ str(x) + "/" + str(tryouts) + "), trying again in 5s...")
            time.sleep(5)
        else :
            # some other error we can't handle here
            raise gp.GPhoto2Error(error)
            logging.error("Gphoto2 error : " + error)
            break

    # Check if all tryouts have run
    if x == tryouts :
        logging.critical("Camera not found. Aborting initilization.")
        return False

    # Get configuration tree
    cameraConfig = gp.check_result(gp.gp_camera_get_config(camera))

    #########
    # Get Camera model
    cameraNameWidget = gp.check_result(
                gp.gp_widget_get_child_by_name(cameraConfig, 'model'))
    cameraName = ""
    cameraName = gp.check_result(
                    gp.gp_widget_get_value(cameraNameWidget))#, cameraName))
    logging.info("Camera model : %s" %cameraName)

    #########
    # Find the capture target config item
    captureTarget = gp.check_result(
        gp.gp_widget_get_child_by_name(cameraConfig, 'capturetarget'))

    value = 1 # 0 is for internal memory, 1 is for SD card
    # Check value in range
    count = gp.check_result(gp.gp_widget_count_choices(captureTarget))
    if value < 0 or value >= count:
        logging.error('Parameter out of range')
        return False
    # set value
    value = gp.check_result(gp.gp_widget_get_choice(captureTarget, value))
    gp.check_result(gp.gp_widget_set_value(captureTarget, value))
    # # set config
    # gp.check_result(gp.gp_camera_set_config(camera, cameraConfig))

    #########
    # Set the autofocusdrive
    # Find the capture target config item
    autoFocusDrive = gp.check_result(
        gp.gp_widget_get_child_by_name(cameraConfig, 'autofocusdrive'))

    autofocus = 1 # 1 is to trigger the AF drive
    # set value
    gp.check_result(gp.gp_widget_set_value(autoFocusDrive, autofocus))


# Captures an image, take the current time and save in into the inputted folder.
# Input : GPhoto camera object, Folder where to save the pictures
# Output : name of the latest picture taken
def takePhoto(camera, pictureFolder):
    #global camera

    logging.info('Capturing image...')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    logging.debug('Picture path on the camera : {0}/{1}'.format(file_path.folder, file_path.name))
    # Get the name of the picture just taken
    pictureFile = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))

    # Build a timestamp to name the picture
    now = time.time()
    timestamp = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d_%H-%M-%S')
    extension = '.jpg'
    newPictureFile = os.path.join(pictureFolder, timestamp + extension)

    # Save the picture to the indicated folder
    gp.check_result(gp.gp_file_save(pictureFile, newPictureFile))
    logging.info('New picture : %s' %newPictureFile)

    return timestamp + extension

# Returns True is the camera battery falls under a threshold
def checkBattery(camera, batt_lvl):
    #global camera, batt_lvl

    # Get configuration tree
    cameraConfig = gp.check_result(gp.gp_camera_get_config(camera))
    # Get Camera model
    batteryLevelWidget = gp.check_result(
                gp.gp_widget_get_child_by_name(cameraConfig, 'batterylevel'))
    batteryLevel = ""
    batteryLevel = gp.check_result(
                    gp.gp_widget_get_value(batteryLevelWidget))#, cameraName))

    if batteryLevel < batt_lvl :
        logging.critical("Battery level too low : %d%" %int(batteryLevel))
        return False
    else :
        logging.info("Battery level : %d%" %int(batteryLevel))
        return True
        # True means battery too low
