# Code snippets

Those are a collection of snippets I fetched during my investigation on how to do it...

---
## List the capabilities of a camera :
`gphoto2 --list-all-config >config.txt`


Display `config.txt` to see what is supported.

---
## Disable IPv6 on Raspberry
Reference [here](https://askubuntu.com/a/309463/217297)


---
## Python Serial port and commands
Reference [here](https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package)

```
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

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

---
## Capture and download using python

From python-gphoto2 [examples](https://github.com/jim-easterbrook/python-gphoto2/blob/master/examples/capture-image.py).
Two functions are used :
* `gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE)`  
to trigger the shot
* `gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)`  
to download the image

```
#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2015-17  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

---
## Serial communication with an Arduino

from [here](https://stackoverflow.com/a/24075787/3494633)

```
#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = '/dev/tty.usbmodem1411' # note I'm using Mac OS-X


ard = serial.Serial(port,9600,timeout=5)
time.sleep(2) # wait for Arduino

i = 0

while (i < 4):
    # Serial write section

    setTempCar1 = 63
    setTempCar2 = 37
    ard.flush()
    setTemp1 = str(setTempCar1)
    setTemp2 = str(setTempCar2)
    print ("Python value sent: ")
    print (setTemp1)
    ard.write(setTemp1)
    time.sleep(1) # I shortened this to match the new value in your Arduino code

    # Serial read section
    msg = ard.read(ard.inWaiting()) # read all characters in buffer
    print ("Message from arduino: ")
    print (msg)
    i = i + 1
else:
    print "Exiting"
exit()
```

---
## Resize image to 1080p

`resize.py` takes car of resizing the image to a FullHD (1920x1080). Inspired from [here](https://www.blog.pythonlibrary.org/2017/10/12/how-to-resize-a-photo-with-python/)
```
# python resize.py
  Original image : 5184x3456
  Scaled image : 1920x1280
  Elapsed time: 1.178s
```

resize.py :
```
from PIL import Image
import time

def scale_image(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    print('Original image : {wide}x{height} '
          'high'.format(wide=w, height=h))

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        # No width or height specified
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('Scaled image : {wide}x{height} '
          'high'.format(wide=width, height=height))


if __name__ == '__main__':

    start = time.time()

    scale_image(input_image_path='2018-11-30_20:12:39.jpg',
                output_image_path='2018-11-30_20:12:39_scaled.jpg',
                width=1920)

    elapsed = time.time() - start
    print 'Elapsed time: %.3fs' % (elapsed)
```


---
## Standalone Photobooth using RPi only

from [here](https://github.com/feiticeir0/RPiPhotoBooth/blob/master/RPiPhotoBooth.py)

```
# Testing here
while (True):
	try:
		camera.start_preview()      # <--- To be replaced by the libphoto function
		#Show LED Only for Take Picture
		onlyTakePicLed()
		# Wait for button to take Picture
		GPIO.wait_for_edge(takeButton,GPIO.FALLING)
		# Start a thread to count with the LEDs while the images are shown
		# Probably could be used in the overlayCounter function,
		# because it also as timers to show the pictures, but the led effects would not
		# be the same
		thread.start_new_thread ( countingTimerPicture,() )

		# Show the pictures overlay in the camera picture
		overlayCounter()
		# Show all LEDS while taking the picture
		showAllLeds()

		# Define a filename and path
		filename = "fotos/%s.jpg" % (time.strftime("%G%m%d%H%M%S"))
		# camera.capture('pushTesting.jpg')
		camera.capture(filename)
		camera.stop_preview()

		#display image
		# Resize and display the resized one
		#filename_t = "fotos/resized_t.jpg"
		# resizeThumbnail(filename)
		displayPreview(filename)
		# Show overlay
		oo = overlaysn()
		# While not choosing an option
		### Add a callback
		####GPIO.add_event_detect(socialNetworkButton,GPIO.FALLING,callback=tweetImage,bouncetime=300)
		###while (True):
		###	GPIO.wait_for_edge(cancelButton, GPIO.FALLING)
		####	print ("cancelled Button")
		##	break
		# Show LEDs to Cancel or Post to Social Networks
		cancelPostLEDS()
		GPIO.add_event_detect(socialNetworkButton,GPIO.FALLING)
		GPIO.add_event_detect(cancelButton,GPIO.FALLING)
		while (True):
			if GPIO.event_detected(socialNetworkButton):
				camera.remove_overlay(oo)
				GPIO.output(cancelButtonLed,False)
				o = displayPreview3('Aenviar.png')
				#print "Social Networks Button"
				# add watermark
				# Only add watermark if sending to social networks
				addWaterMark()
				sendToTwitter()
				sendToFacebook()
				camera.remove_overlay(o)
				break
			if GPIO.event_detected(cancelButton):
				#print "Canceled"
				camera.remove_overlay(oo)
				break

		# reset GPIOS
		GPIO.remove_event_detect(socialNetworkButton)
		GPIO.remove_event_detect(cancelButton)
		GPIO.remove_event_detect(takeButton)
		camera.stop_preview()
	except KeyboardInterrupt:
		print ("Exited...")
		#offLeds()
GPIO.cleanup()
```

---
