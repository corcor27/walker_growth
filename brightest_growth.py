import numpy as np
import pydicom as dicom
import mammogram_image_reader as IMREAD
import growth_model as GROW
import matplotlib.pyplot as plt
import model_utilities as UTILS
import cv2
import region_growth as REGION
from scipy.ndimage import gaussian_filter

"""
image details and abnormalitiy location.
"""
def create_volume_list(time, V0, t0, alpha0):
    volume_list = [V0]
    for t in range(1,time):
        volume = int(round(UTILS.exponential_function(t, t0, V0, alpha0),0))
        volume_list.append(volume)
    change_vol = []
    for vol_in in range(0, len(volume_list)-1):
        ch_vol = volume_list[vol_in + 1] - volume_list[vol_in]
        change_vol.append(ch_vol)
        
        
    return change_vol

        
def possible_pos_array(threashold_image, container_array):
    positions_array = np.zeros((threashold_image.shape))
    for kk in range(1, threashold_image.shape[0]-1):
        for ii in range(1, threashold_image.shape[1]-1):
            if container_array[kk,ii] > 0 and threashold_image[kk,ii] > 0:
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        y, x = kk + dy, ii + dx
                        positions_array[y,x] = threashold_image[y,x] - container_array[y,x]
    return positions_array

def brightness_list(possible_positions, batch_size, container_array):
    template = possible_positions
    for gg in range(0, batch_size):
        max_val = np.amax(template)
        for kk in range(0, possible_positions.shape[0]):
            for ii in range(0, possible_positions.shape[1]):
                if template[kk,ii] == max_val:
                    template[kk,ii] = 0
                    container_array[kk,ii] += 1
                    
               
    return container_array
        
        
    

def brightest_growth(threashold_image, batch_size, req_vol, container_array, count):
    if req_vol < batch_size:
        aval_pos = possible_pos_array(threashold_image, container_array)
        container_array = brightness_list(aval_pos, req_vol, container_array)
    else:
        NOI = int(np.floor(req_vol/batch_size))
        remainder = req_vol - (NOI*batch_size)
        print(NOI)
        for val in range(0, NOI):
            aval_pos = possible_pos_array(threashold_image, container_array)
            container_array = brightness_list(aval_pos, batch_size, container_array)
            output = "/home/a.cot12/modeling/0145_2_batch10/%s.png" %(count)
            plt.imsave(output, container_array, cmap = 'gray')
            count += 1
        aval_pos = possible_pos_array(threashold_image, container_array)
        container_array = brightness_list(aval_pos, remainder, container_array)
        
    return container_array, count

image_path = "/home/a.cot12/Mam_dataset/dicom_M/0145-2.dcm"

x1 = 1372
x2 = 1551
z1 = 1492
z2 = 1674
width = x2 - x1 + 150
height = z2 - z1 + 150
iterations = 10
batch_size = 10
LB = 0
t0 = 0
V0 = 1
alpha0 = 0.5
beta = 0.05 
LB = 0

image = IMREAD.diread_area(image_path,x1,x2,z1,z2, LB)
binary_image = UTILS.IMAGE_THREASHOLD_OTSU(image)
threashold_image = REGION.grow_region(image, binary_image)
Vc = IMREAD.threashold_volume(threashold_image)
time = UTILS.time_exponential_function(t0, V0, alpha0, Vc)

Centre_start = UTILS.Centre_start(threashold_image)
container_array = UTILS.inialise_2d_array(Centre_start[0],Centre_start[1], height, width)
volume_list = create_volume_list(time, V0, t0, alpha0)
count = 1
for vol in volume_list:
    container_array, count = brightest_growth(threashold_image, batch_size, vol, container_array, count)
    
    count +=1
    
    
    

    
