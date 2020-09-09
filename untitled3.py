import os
import sys
import random

import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import csv


path = r"D:\Documents\dataset-skunet\UDIAT\Benign\mask"
path1 = r"D:\Documents\dataset-skunet\UDIAT\Malignant\mask"

benign = os.listdir(path)
malignant = os.listdir(path1)
length_benign = len(benign)
length_malignant = len(malignant)
ROI_area_benign = []
ratio_area_benign = []
ROI_area_malignant = []
ratio_area_malignant = []
for kk in range(0, length_benign):
    mask_path = os.path.join(path,benign[kk])
    mask_image = cv2.imread(mask_path,0)
    mask_area = area(mask_image)
    ROI_area_benign.append(mask_area[0])
    ratio_area_benign.append(mask_area[1])
    
for ii in range(0, length_malignant):
    mask_path = os.path.join(path1,malignant[ii])
    mask_image = cv2.imread(mask_path,0)
    mask_area = area(mask_image)
    ROI_area_malignant.append(mask_area[0])
    ratio_area_malignant.append(mask_area[1])
print(ROI_area_malignant)    
data = [ratio_area_benign, ratio_area_malignant] 
colors = ['#FFFF00', '#FFFF00']#, '#FFFF00', '#FFFF00']   

fig = plt.figure(figsize =(5, 5)) 
  
# Creating axes instance 
ax = fig.add_axes([0, 0, 1, 1]) 
ax.set_xticklabels(['Benign', 'Malignant'])
plt.title("UDIAT")
# Creating plot 
bp = ax.boxplot(data, patch_artist = True, 
                notch ='True') 
  
# show plot 
plt.show() 
