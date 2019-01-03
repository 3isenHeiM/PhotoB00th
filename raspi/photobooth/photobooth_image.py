#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
import skimage
from skimage import io, filters
# from skimage.viewer import ImageViewer
import numpy as np
import time
import os, os.path
import logging

#     scale_image(input_image_path='2018-11-30_20:12:39.jpg',
#                output_image_path='2018-11-30_20:12:39_scaled.jpg',
#                width=1920)


processedFolder = "images/processed"
imageFolder     = "images/jpg"
image_count     = "image_count.txt"
count           = 0
enableFilter     = True

# Reads the image count from the file
def getImageCount():
    file = open(image_count, 'r').readline()
    count = int(file)

# Updates the integer of the count of images in the folder.
def updateImageCount():
    file = open(image_count, 'w')
    file.write(str(count) + "\n")
    file.close()

def resizePicture(input_image_path,
                output_image_path,
                width=None,
                height=None
                ):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    logging.debug('Original picture : {wide}x{height}px '
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
    logging.info('Picture resized to {wide}x{height}px'.format(wide=width, height=height))

#################################################################
# INSTAGRAM GOTHAM FILTER
# from https://github.com/3isenHeiM/CV-Instagram-Filters
#################################################################

# Inputs :
# * Path to the input image
# * Path to the output image


# To suppress the warning :
#       UserWarning: Possible precision loss when converting from float64 to uint8
# Run with $python -W ignore gotham.py

def split_image_into_channels(image):
    """Look at each image separately"""
    red_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]
    return red_channel, green_channel, blue_channel


def merge_channels(red, green, blue):
    """Merge channels back into an image"""
    return np.stack([red, green, blue], axis=2)


def sharpen(image, a, b):
    """Sharpening an image: Blur and then subtract from original"""
    blurred = skimage.filters.gaussian(image, sigma=10, multichannel=True)
    sharper = np.clip(image * a - blurred * b, 0, 1.0)
    return sharper


def channel_adjust(channel, values):
    # preserve the original size, so we can reconstruct at the end
    orig_size = channel.shape
    # flatten the image into a single array
    flat_channel = channel.flatten()

    # this magical numpy function takes the values in flat_channel
    # and maps it from its range in [0, 1] to its new squeezed and
    # stretched range
    adjusted = np.interp(flat_channel, np.linspace(0, 1, len(values)), values)

    # put back into the original image shape
    return adjusted.reshape(orig_size)

def applyFilter(imageFile,filteredImage):
    # 0. Open the image
    original_image = skimage.io.imread(imageFile)
    original_image = skimage.util.img_as_float(original_image)


    # 1. Colour channel adjustment example
    r, g, b = split_image_into_channels(original_image)
    r_interp = channel_adjust(r, [0, 0.8, 1.0])
    red_channel_adj = merge_channels(r_interp, g, b)

    # 2. Mid tone colour boost
    r, g, b = split_image_into_channels(original_image)
    r_boost_lower = channel_adjust(r, [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0])
    r_boost_img = merge_channels(r_boost_lower, g, b)

    # 3. Making the blacks bluer
    bluer_blacks = merge_channels(r_boost_lower, g, np.clip(b + 0.03, 0, 1.0))

    # 4. Sharpening the image
    #       This takes most of the time
    sharper = bluer_blacks
    #sharper = sharpen(bluer_blacks, 1.3, 0.3)

    # 5. Blue channel boost in lower-mids, decrease in upper-mids
    r, g, b = split_image_into_channels(sharper)
    b_adjusted = channel_adjust(b, [0, 0.047, 0.118, 0.251, 0.318, 0.392, 0.42, 0.439, 0.475, 0.561, 0.58, 0.627, 0.671, 0.733, 0.847, 0.925, 1])
    gotham = merge_channels(r, g, b_adjusted)

    # 6. Save the images
    skimage.io.imsave(filteredImage, gotham)
    logging.info("Picture saved to %s" %filteredImage)



def postProcess(imageFile):
    global count
    start = time.time()

    # Increment the counter for the webserver
    count = count + 1
    updateImageCount()

    newPictureName = str(count) + ".jpg"
    newPictureFile = os.path.join(processedFolder, newPictureName)

    if not enableFilter :
        # No Filter, the resizing outputs directly in the processed folder
        resizePicture(os.path.join(imageFolder, imageFile),
            newPictureFile, width=1920)
    else :
        # Insert "_scaled" at the end of the picture name (temp file)
        [imageName, extension] = os.path.splitext(imageFile)
        resizedImage = imageName + "_scaled" + extension

        # Resize the picture
        resizePicture(os.path.join(imageFolder, imageFile),
                os.path.join(imageFolder, resizedImage), width=1920)

        # Delete original file
        os.remove(os.path.join(imageFolder, imageFile)) 

        # Apply Instagram filter and moved the picture in the proceesed folder
        applyFilter(os.path.join(imageFolder, resizedImage), newPictureFile)

    elapsed = time.time() - start
    logging.info("Picture processing time : %.3fs" %elapsed)
