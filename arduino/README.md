# Arduino Photobooth

This is part of the Photob00th but might be used standalone.

The Arduino interfaces will all the GPIOs (LED, buttons, etc...) and commmunicates via a Serial port with the Raspberry.

The Arduino is used to be able to dim the lisght of the big 4 LEDs. The dim is done using PWM modulation. I could not find any resources online to execute this on the RaspBerry (with 12V LEDs).

## State machine
cf main ReadMe.md


## Wiring Diagram
![Arduino Photobooth](https://raw.githubusercontent.com/3isenHeiM/Photob00th/master/arduino/arduino_photobooth.jpg)




## PWM explanation
* [Controlling an LED by PWM](https://www.sunfounder.com/learn/Super-Kit-V2-0-for-Arduino/lesson-3-controlling-an-led-by-pwm-super-kit.html)
* [Fade an LED with Pulse Width Modulation using analogWrite()](https://programmingelectronics.com/tutorial-10-fade-an-led-with-pulse-width-modulation-using-analogwrite/)
