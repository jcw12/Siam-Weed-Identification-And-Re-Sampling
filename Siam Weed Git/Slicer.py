# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:38:11 2023

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 11:20:53 2021

@author: dgautam
"""

# import image_slicer



# image_slicer.slice('DJI_0247.JPG', 96)

# function inputs = image, desired size, desired numbersx desired numbery

import cv2
import math
import os

inputFolder = r"C:\Users\user\Documents\GitHub\Siam-Weed-Identification-And-Re-Sampling\Siam Weed Git\UnSliced"
outputFolder = r"C:\Users\user\Documents\GitHub\Siam-Weed-Identification-And-Re-Sampling\Siam Weed Git\Regular"

#Set downsampling method and downsampling factor here:
Downsampling = False
#Options for method include INTER_CUBIC, INTER_LANCZOS4, INTER_LINEAR
Method = cv2.INTER_LANCZOS4
Factor = 2

#Tile Sizes:
tile_size = (456, 456)
offset = (456, 456) # the size of image must be divisible by the offset value. Offset value closer to the tile_size but can be marginally less - not more.

def sliceEmAll(imageName, img):
    #img = cv2.imread(imageName)
    img_shape = img.shape
    #This function slices an image into m*n tiles. The code is adopted from https://stackoverflow.com/questions/45950124/creating-image-tiles-mn-of-original-image-using-python-and-numpy
    for i in range(int(math.ceil(img_shape[0]/(offset[1] * 1.0)))):
        for j in range(int(math.ceil(img_shape[1]/(offset[0] * 1.0)))):
            cropped_img = img[offset[1]*i:min(offset[1]*i+tile_size[1], img_shape[0]), offset[0]*j:min(offset[0]*j+tile_size[0], img_shape[1])]
            # Debugging the tiles
            #print(img)
            print(imageName)
            outputImagePath = imageName.replace(inputFolder+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
            #outputImagePath = imageName.replace("\\","_").replace(inputFolder+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
            print(outputImagePath)
            cv2.imwrite(outputImagePath, cropped_img)
    return 0

def load_images_from_folder(folder):
    inputImages = []
    for path, subdirs, files in os.walk(inputFolder):
        for name in files:
            img = cv2.imread(os.path.join(path, name))
            if img is not None:
                print(5)
                print(os.path.join(path, name))
                inputImages.append(os.path.join(path, name))
                #Resample Here
                print(os.path.join(path, name),path,name)
                if Downsampling == True:
                    downsample(os.path.join(path, name))
                else:
                    sliceEmAll(os.path.join(path, name), img)
                    
                    
                
                                   
                #
    return inputImages


def downsample(image):
    #https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    #https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
    img = cv2.imread(image)
    width = int(img.shape[1] / Factor)
    height = int(img.shape[0] / Factor)
    shape = (width, height)
    img = cv2.resize(img, shape, interpolation = Method)
    sliceEmAll(image, img)
    
    

    
    
    
    
    
inputImages = load_images_from_folder(inputFolder)
    
    
    
    
# downsampling
# original 2 cm
# output pixel 4 cm
# output 8 cm pixel 

#dipsgautam@gmail.com
       
       


    
