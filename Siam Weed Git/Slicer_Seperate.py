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

"""
Need to make it all one function, where the downsampling method can be chosen and the factor can be chosen,
with a factor of 1 as an option. Also need to adjust the ends so that the moving window doesn't clip the ends.'
"""

#Options for method include cv2.INTER_CUBIC, cv2.INTER_LANCZOS4, cv2.INTER_LINEAR, 'PIXEL_AGG'. PIXEL_AGG is the recommended method for most realistic upscaled images.
Method = 'PIXEL_AGG'
Factor = 5

#Tile Sizes:
tile_size = (456, 456)
offset = (456, 456) # the size of image must be divisible by the offset value. Offset value closer to the tile_size but can be marginally less - not more.

def Slicer (imageName, outputFolder, tile_size=(456,456), offset=None, offset_shift = True):
    print ("""
--- Slicing Image ---""")
    if offset == None:
        offset = tile_size
    if type(imageName) == str:
        img = cv2.imread(imageName)
    else:
        img = imageName
    img_shape = img.shape
    print('Slicing Now with Tile Size:', tile_size, 'and Window Offset:', offset)
    
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
        
        
    #This function slices an image into m*n tiles. The code is adopted from https://stackoverflow.com/questions/45950124/creating-image-tiles-mn-of-original-image-using-python-and-numpy
    for i in range(int(math.ceil(img_shape[0]/(offset[1] * 1.0)))):
        if offset_fit_0 != 0 and i == math.ceil(img_shape[0]/(offset[1] * 1.0))-1:
        
            window_top = offset[1]*i-(tile_size[0]-offset_fit_0)
            print('window_top:',window_top)
            window_height = min(offset[1]*i+tile_size[1], img_shape[0])
            print('here')
        else:
            window_top = offset[1]*i
            print('window_top:',window_top)
            window_height = min(offset[1]*i+tile_size[1], img_shape[0])
        for j in range(int(math.ceil(img_shape[1]/(offset[0] * 1.0)))):
            print(offset*j)
            print(math.ceil(img_shape[1]/(offset[1] * 1.0)))
            #If offsets need to be made and it's the last window
            if offset_fit_1 != 0 and j == math.ceil(img_shape[1]/(offset[0] * 1.0))-1:
                print('Adjust this!', i,j)
                window_start = offset[0]*j-(tile_size[1]-offset_fit_1)
                window_length = min(offset[0]*j+tile_size[0], img_shape[1])
            else:
                window_start = offset[0]*j
                window_length = min(offset[0]*j+tile_size[0], img_shape[1])
            cropped_img = img[window_top:window_height, window_start:window_length]
            # Debugging the tiles
            #print(img)
            print(imageName)
            if type(imageName) == str:
                print('Writing output image:', imageName.replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png"))
                outputImagePath = imageName.replace(os.path.dirname(imageName)+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
            else:
                print('Writing output image:', imageName.replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png"))
                
           
            #outputImagePath = imageName.replace("\\","_").replace(inputFolder+"\\",outputFolder+"\\").replace(".JPG","_"+str(i+1) + "_" + str(j+1) + ".png")
            cv2.imwrite(outputImagePath, cropped_img)
    print('Slicer Complete')
    return 0

def load_images_from_folder(inputFolder):
    inputImages = []
    for path, subdirs, files in os.walk(inputFolder):
        for name in files:
            img = cv2.imread(os.path.join(path, name))
            if img is not None:
                print("""
            --- Loading Image ---""")
                inputImages.append(os.path.join(path, name))
                print('Image', name, 'Loaded')
                    
                                   
                #
    return inputImages

def downsample(img, Downsampling_method, Factor, outputFile = None):
    data = cv2.imread(img)
    print ("""
--- Downsampling Image ---""")
    print('downsample data shape', data.shape)
    aggregation_factor = Factor
    if Method == 'PIXEL_AGG' and Downsampling == True:
        print('Downsampling using', Method, 'and a scale factor of',Factor)
        # Compute the padding required
        padding_rows = data.shape[0] % aggregation_factor
        padding_cols = data.shape[1] % aggregation_factor
        print('Downsample Clipping:',padding_rows,padding_cols)
        # Pad the array with zeros
        #padded_data = np.pad(data, ((0, padding_rows), (0, padding_cols), (0, 0)), mode='constant')
        #print('padded:',padded_data.shape)
        
        padded_data = data[:data.shape[0]-padding_rows,:data.shape[1]-padding_cols,:3]
        print('clipped:',padded_data.shape)
        # Reshape the padded ndarray
        reshaped_data = padded_data.reshape(padded_data.shape[0] // aggregation_factor, aggregation_factor,
                                        padded_data.shape[1] // aggregation_factor, aggregation_factor, data.shape[2])
        
        # Compute the mean along the specified axes
        print('Old Shape:', data.shape)
        data = np.mean(reshaped_data, axis=(1, 3))
        print('New Shape:', data.shape)
        print('Clipping to make downsampling factor fit:',padding_rows,padding_cols)
    elif Downsampling == True:
        print('Downsampling using', Method, 'and a scale factor of',Factor)
        #https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
        #https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
        width = int(data.shape[1] / Factor)
        height = int(data.shape[0] / Factor)
        shape = (width, height)
        data = cv2.resize(data, shape, interpolation = Method)
        
    else:
        print('Not Downsampling.')
    if outputFile != None:
        print('Outputting downsampled image to', outputFile)
        cv2.imwrite(outputFile, data)
    else:
        return data
    print('Downsampling Complete')

print('Script complete, functions loaded')
 
# downsampling
# original 2 cm
# output pixel 4 cm
# output 8 cm pixel 

#dipsgautam@gmail.com
#jcurrie987@gmail.com
       
       


    
