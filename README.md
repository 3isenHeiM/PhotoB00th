# Photob00th

A RPi photobooth for my brother's wedding, that controls a DSLR and makes a slideshow of the pictures.

Forked from kitesurfer1404's one.

Architecture : RPI for interfacing the DSLR, with arduino to command the I/Os.


## Required features
By order of importance...
* RaspberryPi-based
* Pictures from DSLR (and not Picamera module)
* LED light (because the room will be dark)
* Press button to trigger capture
* Publish the photos as slideshow on a (remote) screen
* Countdown (7-segment display ?)
* Do a Wooden enclosure

## Design

* RaspberryPi : 
  * Controls the DLSR
  * Setup the slideshow
* Arduino :
  * Wait for events on the button (+ light it up with the countdown)
  * Control the 7-segment display
  * Light and dim the big LEDs

* Serial link between Arduino and RaspberryPi to exchagne commands and feeback.
* State machine running on both µcontrollers to listen for serial commands
* based on serial commands, they can interact

## Sources :
* [Control 7-segment display using python](https://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python)
* [Example Contorl big button + light](https://photos.google.com/share/AF1QipOwxhytRgeDRXFwA8Ee42yeQ1euaZ-cLYzybYsmrUi8KKORaJuT7p9L6YDLRAZysg?key=M21aS3pQQjdpRG1kOW1rbjFnOWdjWldQTEpFVGtR)


## Bill of Materials :
* [Big Red Arcade button](https://www.adafruit.com/product/1185) - Adafruit
* [Big Red dome button](https://www.sparkfun.com/products/9181) - Sparkfun - 11.95$
  12V supply
* [7-Segment display 6,5"](https://www.sparkfun.com/products/8530) - Sparkfun - 18.95$
  12V supply
* [Jumper wires M/F](https://www.sparkfun.com/products/9140) - Sparkfun - 3.95$
  10x 6,5" Jumper cables Male/Female (to connect with RPi)
* 4 LED MR16 Spotlight 12V 4W
* [10pc MR16 Sockets](https://www.amazon.com/Glo-shine-Halogen-Ceramic-Connector-Adapter/dp/B00Y7GRGZ0) - Amazon - 7.71$

## Workflow
Here is the workflow I intially intend for this project :
1. Push the red button
2. Countdown from 3 to 0 :
    - Count using the 7-segment display
    - Light up/down the red button
    - Light the LEDs
    - At "1", ask the RPi to do the focus
    - Display the camera preview on a VGA screen
3. Trigger picture and light the LEDs more
4. Downlaoad the picture (raw/jpg?) on the RaspberryPi's external storage
5. Move a jpg version to the webserver backend
6. Reset the setup

### Arduino State machine

Initial state : 
    * LED dimmed (around 25%)
    * Wait for event on the button

1. When button is pressed :  
    - Display "3" on 7-segment display for 1s
    - Light the LEDs up
    - Light the button for 0.5s
2. After 1s :
    - Display "2" on the 7-segment display for 1s
    - Light the button for 0.5s
3. After 1s : 
    - Display "1" on the 7-segment display for 1s
    - Send commant "`do_focus`" via serial to the RPi
    - Light the button for 0.5s
4. Take the photo : 
     - Increase lights of the LED to 100%
    - Send command "`take_picture`" via serial to the RPi
    - Wait for command "`picture_taken`" from the serial port
5. Get back to initial state

### Raspberry Pi State machine

Initial state : 
* Waiting for command "`do_focus`" from the Arduino

1. When `do_focus` si received :
* use gphoto to do the focus (not sure if supported)
2. When `take-picture` is received : 
* use gphoto to `capture-image-and-download`
3. Post-process the image :
* Move it the the correct folder
* Rename it
* Update the slideshow
4. Get back to initial state

## Stepping stones
* Dimm the 12V LEDs using the Raspberry and a Darlington array (since they are 12V-powered)
    Solution : Use an Arduino Uno for all GPIO-related events.
