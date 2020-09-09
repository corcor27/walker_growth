import numpy as np
import pydicom as dicom
import mammogram_image_reader as IMREAD
import matplotlib.pyplot as plt
from skimage import io
import skimage
import cv2
import os
import shutil


image_path = r"D:\Documents\dataset-skunet\UDIAT\dataset1\image"
mask_path = r"D:\Documents\dataset-skunet\UDIAT\dataset1\mask"

pathmimage = r"D:\Documents\dataset-skunet\UDIAT\d1m\image"
pathmmask = r"D:\Documents\dataset-skunet\UDIAT\d1m\mask"
pathbimage = r"D:\Documents\dataset-skunet\UDIAT\d1b\image"
pathbmask = r"D:\Documents\dataset-skunet\UDIAT\d1b\mask"
count = 0
mask_list = os.listdir(image_path)
for ii in range(0, len(mask_list)):
    if 'malignant.png' in mask_list[ii]:
        output_mask = os.path.join(pathmmask, mask_list[ii])
        output_image = os.path.join(pathmimage, mask_list[ii])
        path_to_mask = os.path.join(mask_path, mask_list[ii])
        path_to_image = os.path.join(image_path, mask_list[ii])
        shutil.copyfile(path_to_mask, output_mask)
        shutil.copyfile(path_to_image, output_image)
    
    else:
        output_mask = os.path.join(pathbmask, mask_list[ii])
        output_image = os.path.join(pathbimage, mask_list[ii])
        path_to_mask = os.path.join(mask_path, mask_list[ii])
        path_to_image = os.path.join(image_path, mask_list[ii])
        shutil.copyfile(path_to_mask, output_mask)
        shutil.copyfile(path_to_image, output_image)