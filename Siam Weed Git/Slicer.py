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

import cv2
import math
import os
import numpy as np


#Options for method include cv2.INTER_CUBIC, cv2.INTER_LANCZOS4, cv2.INTER_LINEAR, 'PIXEL_AGG'. PIXEL_AGG is the recommended method for most realistic upscaled images.

"""
Required parameters: Input Folder, Output Folder.
Optional parameters: Tilesize, Offset, Offset Shift, [Downsampling method, Factor]
If optional parameters aren't specifed:
    Tilesize: 456,456
    Offset: Offset is the same as the Tilesize
    Offset Shift: True
    [Downsampling_method, Factor]: No downsampling
    #
"""

def Slicer(inputFolder, outputFolder, tile_size=(456,456), offset=None, offset_shift = True, Downsampling = [0,1]):
    if offset == None:
        offset = tile_size
    #Split the downsampling argument into the Method and Factor components
    Method = Downsampling[0]
    Factor = Downsampling[1]
    
    #Load the images from input folder
    print("""
--- Loading Image ---""")
    inputImages = []
    for path, subdirs, files in os.walk(inputFolder):
        for name in files:
            img = cv2.imread(os.path.join(path, name))
            if img is not None:
                inputImages.append(os.path.join(path, name))
                print('Image', name, 'Loaded')
                
                #Check if downsampling is required and downsample if necessary
                if Method != 0 and Factor != 1:
                    print ("""
--- Downsampling Image ---""")
                    img = os.path.join(path, name)
                    data = cv2.imread(img)
                    aggregation_factor = Factor
                    if Method == 'PIXEL_AGG':
                        print('Downsampling using', Method, 'and a scale factor of',Factor,'.')
                        # Compute the clipping required
                        padding_rows = data.shape[0] % aggregation_factor
                        padding_cols = data.shape[1] % aggregation_factor
                        
                        # Pad the array with zeros
                        #padded_data = np.pad(data, ((0, padding_rows), (0, padding_cols), (0, 0)), mode='constant')
                        #print('padded:',padded_data.shape)
                        
                        padded_data = data[:data.shape[0]-padding_rows,:data.shape[1]-padding_cols,:3]
                        
                        print('Old Shape:', data.shape)
                        # Reshape the clipped ndarray
                        data = padded_data.reshape(padded_data.shape[0] // aggregation_factor, aggregation_factor,
                                                        padded_data.shape[1] // aggregation_factor, aggregation_factor, data.shape[2])
                        # Compute the mean along the specified axes
                        img = np.mean(data, axis=(1, 3))
                        print('New Shape:', img.shape)
                        print('Clipping to make downsampling factor fit:',padding_rows,padding_cols)
                    else:
                        print('Downsampling using', Method, 'and a scale factor of',Factor)
                        #https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
                        #https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
                        width = int(data.shape[1] / Factor)
                        height = int(data.shape[0] / Factor)
                        shape = (width, height)
                        img = cv2.resize(data, shape, interpolation = Method)
                
                
                #Slice the image
                print ("""
--- Slicing Image ---""")
                print('Slicing Now with Tile Size:', tile_size, 'and Window Offset:', offset)
                imageName = os.path.join(path, name)
                img_shape = img.shape
                
                #Find the fitness of the offset to confirm whether or not the last tile will need to be shifted, and identify the amount of shift necessary
                if offset_shift == True:
                    offset_fit_0 = img_shape[0] % offset[0]
                    offset_fit_1 = img_shape[1] % offset[1]
                    if offset_fit_0 != 0 or offset_fit_1 != 0:
                        print('offset shift:',offset_fit_0, offset_fit_1, 'Final Tile(s) Position will be adjusted to maintain tile size.')
                    else:
                        print('offset shift:',offset_fit_0, offset_fit_1, 'Final Tile(s) Position not adjusted.')
                else:
                    offset_fit_0 = 0
                    offset_fit_1 = 0
                
                
                #This function slices an image into m*n tiles. The code is adopted from https://stackoverflow.com/questions/45950124/creating-image-tiles-mn-of-original-image-using-python-and-numpy but has been adapted to include the offset shift function.
                for i in range(int(math.ceil(img_shape[0]/(offset[1] * 1.0)))):
                    if offset_fit_0 != 0 and i == math.ceil(img_shape[0]/(offset[1] * 1.0))-1:
                        window_top = offset[1]*i-(tile_size[0]-offset_fit_0)
                        window_height = min(offset[1]*i+tile_size[1], img_shape[0])
                    else:
                        window_top = offset[1]*i
                        window_height = min(offset[1]*i+tile_size[1], img_shape[0])
                    for j in range(int(math.ceil(img_shape[1]/(offset[0] * 1.0)))):
                        #If offsets need to be made and it's the last window
                        if offset_fit_1 != 0 and j == math.ceil(img_shape[1]/(offset[0] * 1.0))-1:
                            window_start = offset[0]*j-(tile_size[1]-offset_fit_1)
                            window_length = min(offset[0]*j+tile_size[0], img_shape[1])
                        else:
                            window_start = offset[0]*j
                            window_length = min(offset[0]*j+tile_size[0], img_shape[1])
                        cropped_img = img[window_top:window_height, window_start:window_length]

                        outputImagePath = imageName.replace(inputFolder+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
                        #SUPERSEDED - outputImagePath = imageName.replace("\\","_").replace(inputFolder+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
                        print('Writing output image:', name.replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png"))
                        cv2.imwrite(outputImagePath, cropped_img)
    print('Slicer Complete')

#dipsgautam@gmail.com
#jcurrie987@gmail.com
print('Slicer scipt run and functions loaded')

#Slicer(r'C:\Users\user\Documents\GitHub\Siam-Weed-Identification-And-Re-Sampling\Siam Weed Git\UnSliced',r'C:\Users\user\Documents\GitHub\Siam-Weed-Identification-And-Re-Sampling\Siam Weed Git\Test')

    
