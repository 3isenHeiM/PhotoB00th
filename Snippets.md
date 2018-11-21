# Code snippets

## Arduino

### Wait for event on button 

from [here](https://arduino.stackexchange.com/a/15846)
```
while (digitalRead(A2) == HIGH) {
  // Do nothing
}
```

### Make the button fade in/out whilne nobody pushes it

from [here](https://learn.sparkfun.com/tutorials/reaction-timer)

```
//If there is no game going on, pulse the LED on/off
//If the user ever presses the button then return immediately
//This function takes approximately 6 seconds to complete
void pulseTheButton(void)
{
    //Fade LED on
    for(int fadeValue = 0 ; fadeValue <= 255; fadeValue += 5)
    {
        if(digitalRead(button) == LOW) return;

        analogWrite(LED, fadeValue);
        delay(30);
    }

    //Fade LED off
    for(int fadeValue = 255 ; fadeValue >= 0; fadeValue -= 5)
    {
        if(digitalRead(button) == LOW) return;

        analogWrite(LED, fadeValue);
        delay(30);
    }

    //Turn LED off for awhile
    for(int x = 0 ; x < 100 ; x++)
    {
        if(digitalRead(button) == LOW) return;

        analogWrite(LED, 0);
        delay(30);
    }
}
```


## RaspberryPi

### Control leds and camero on RPi
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
