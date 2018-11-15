# Code snippets

Those are a collection of snippets I fetched during my investigation on how to do it...


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
