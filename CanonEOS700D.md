# Canon EOS 700D and gphoto2

` gphoto2 --capture-image-and-download --filename "%Y-%m-%d %H:%M:%S.jpg" `

## Supported operations
```
gphoto2 --list-config
/main/actions/syncdatetimeutc
/main/actions/syncdatetime
/main/actions/uilock
/main/actions/autofocusdrive
/main/actions/manualfocusdrive
/main/actions/cancelautofocus
/main/actions/eoszoom
/main/actions/eoszoomposition
/main/actions/viewfinder
/main/actions/eosremoterelease
/main/actions/opcode
/main/settings/datetimeutc
/main/settings/datetime
/main/settings/reviewtime
/main/settings/output
/main/settings/movierecordtarget
/main/settings/evfmode
/main/settings/ownername
/main/settings/artist
/main/settings/copyright
/main/settings/customfuncex
/main/settings/focusinfo
/main/settings/focusarea
/main/settings/autopoweroff
/main/settings/depthoffield
/main/settings/capturetarget
/main/settings/capture
/main/status/serialnumber
/main/status/manufacturer
/main/status/cameramodel
/main/status/deviceversion
/main/status/vendorextension
/main/status/model
/main/status/ptpversion
/main/status/Battery Level
/main/status/batterylevel
/main/status/lensname
/main/status/eosserialnumber
/main/status/shuttercounter
/main/status/availableshots
/main/imgsettings/imageformat
/main/imgsettings/imageformatsd
/main/imgsettings/iso
/main/imgsettings/whitebalance
/main/imgsettings/colortemperature
/main/imgsettings/whitebalanceadjusta
/main/imgsettings/whitebalanceadjustb
/main/imgsettings/whitebalancexa
/main/imgsettings/whitebalancexb
/main/imgsettings/colorspace
/main/capturesettings/exposurecompensation
/main/capturesettings/focusmode
/main/capturesettings/continuousaf
/main/capturesettings/aspectratio
/main/capturesettings/storageid
/main/capturesettings/highisonr
/main/capturesettings/autoexposuremode
/main/capturesettings/drivemode
/main/capturesettings/picturestyle
/main/capturesettings/aperture
/main/capturesettings/shutterspeed
/main/capturesettings/meteringmode
/main/capturesettings/bracketmode
/main/capturesettings/aeb
/main/other/d402
/main/other/d407
/main/other/d406
/main/other/d303
/main/other/5001
```

## Various operations

### Battery Level
I think that the camera is powered by the UBS cable, so there's no worry about running out of battery when it's USB-connected.
```
# gphoto2 --get-config batterylevel
Label: Battery Level
Readonly: 1
Type: TEXT
Current: 100%
END
```
### AutoPowerOff

```
# gphoto2 --get-config autopoweroff
Label: Auto Power Off
Readonly: 0
Type: TEXT
Current: 30
END
```

### Set Manual Focus
`--set-config manualfocusdrive=Mode` where mode is "Near 1" "Near 2" "Near 3" "Far 1" "Far 2" "Far 3".
These are 3 different relative stepsizes for both focusing directions. To achieve focusing, multiple calls might need to be done.

### Time difference

1. Capture target on internal memory  
`gphoto2 --set-config-index /main/settings/capturetarget=1`  

```
time gphoto2 --capture-image-and-download --filename "%Y-%m-%d_%H:%M:%S.jpg"
New file is in location /store_00020001/DCIM/100CANON/IMG_2523.JPG on the camera
Saving file as 2018-11-30_21:22:42.jpg
Deleting file /store_00020001/DCIM/100CANON/IMG_2523.JPG on the camera
gphoto2 --capture-image-and-download --filename "%Y-%m-%d_%H:%M:%S.jpg"  0.13s user 0.15s system 4% cpu 6.517 total
```
2. Capture target on SD card  
`gphoto2 --set-config-index /main/settings/capturetarget=0`  

```
time gphoto2 --capture-image-and-download --filename "%Y-%m-%d_%H:%M:%S.jpg"
New file is in location /capt0000.jpg on the camera
Saving file as 2018-11-30_20:18:22.jpg
Deleting file /capt0000.jpg on the camera
gphoto2 --capture-image-and-download --filename "%Y-%m-%d_%H:%M:%S.jpg"  0.14s user 0.11s system 7% cpu 3.431 total
```


## Useful links
* [gphoto on MacOS](http://photolifetoys.blogspot.com/2012/08/control-your-camera-with-gphoto2-via.html)
