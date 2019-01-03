# Installation

For the oroginal project I used an Odroid C2 instead of a RapsberryPi 3B+.

This is thus divide din to 2 parts :
* Installation on Odroid C2
* Installation on raspberry Pi

## Installation on Odroid C2

### Installation of GPhoto

Installation of libgphoto-device
`$ sudo apt install gphoto2 libgphoto2-dev`

Installation of gphoto using pip (from [here](https://github.com/jim-easterbrook/python-gphoto2#install-with-pip))
`$ sudo pip install gphoto2`

### Use RPi.GPIO

TO use the GPIOs on the Odroid C2, first we have to install a library to allow us tu ose the same libreary as for the Rapsberry Pi. Useful doc is (here)[https://github.com/jfath/RPi.GPIO-Odroid]


### Installation of Skimage on Odroid C2
1. Install SciPy following [this guide](https://www.scipy.org/install.html). basically running this :  
`sudo apt-get install python-numpy python-scipy python-matplotlib ipython python-pandas python-sympy python-nose`

2. Install Cython (required to build scikit-image)  
`apt install cython`

3. Install `scikit-image` (new version of `skimage`)  
`pip install scikit-image`
