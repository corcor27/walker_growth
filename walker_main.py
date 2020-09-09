import numpy as np
import pydicom as dicom
import walker_growth as GROW
import matplotlib.pyplot as plt
import walker_utilities as UTILS
import cv2
from scipy.ndimage import gaussian_filter
"""
image details and abnormalitiy location.
"""
image_path = "/home/a.cot12/Mam_dataset/dicom_M/1487-1.dcm"

x1 = 214
x2 = 417
z1 = 1034
z2 = 1262
width = x2 - x1 + 150
height = z2 - z1 + 150
iterations = 10

LB = 0
t0 = 0
V0 = 1
alpha0 = 0.5
beta = 0.05 
LB = 0
image = UTILS.diread_area(image_path,x1,x2,z1,z2, LB)

binary_image = UTILS.IMAGE_THREASHOLD_OTSU(image)
threashold_image = UTILS.grow_region(image, binary_image)
dis = UTILS.estimate_distance(threashold_image, 200)


Vc = UTILS.threashold_volume(threashold_image)
time = UTILS.time_exponential_function(t0, V0, alpha0, Vc) + 4
scale= int(round(dis/time))
delay_start = 10 * scale
scaled_time = (time * scale)
walker_array = np.zeros((2, 1), dtype = np.int16)

Centre_start = UTILS.centre_start(threashold_image)
walker_array[:, 0] = [Centre_start[0], Centre_start[1]]
container_array = UTILS.inialise_2d_array(Centre_start[0],Centre_start[1], height, width)


for t in range(delay_start, scaled_time):
    epoch_time = t/scale
    GV = int(round(UTILS.exponential_function(epoch_time, t0, V0, alpha0),0))
    container_array, walker_array = GROW.RUN_RANDOM_GROWTH(container_array, walker_array, threashold_image, height, width, GV)
    if epoch_time == int(epoch_time):
        output = "/home/a.cot12/modeling/0145_2_walkers/%s.png" %(epoch_time)
        plt.imsave(output, container_array, cmap = 'gray')
	
    if (np.sum(container_array)/Vc) >= 0.98:
        break

output = "/home/a.cot12/modeling/1487_1_walkers/final.png" 
output1 = "/home/a.cot12/modeling/1487_1_walkers/threashold_image_1487.png" 
output2 = "/home/a.cot12/modeling/1487_1_walkers/base_image_1487.png" 
plt.imsave(output, container_array, cmap = 'gray')
plt.imsave(output1, threashold_image , cmap = 'gray')
plt.imsave(output2, image , cmap = 'gray')


plt.imshow(template)
