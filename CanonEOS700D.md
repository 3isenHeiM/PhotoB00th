# Canon EOS 700D and gphoto2

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
## Useful links
* [gphoto on MacOS](http://photolifetoys.blogspot.com/2012/08/control-your-camera-with-gphoto2-via.html)
