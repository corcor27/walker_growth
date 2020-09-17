import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import walker_utilities as UTILS
import cv2
from scipy.ndimage import gaussian_filter
from datetime import datetime
startTime = datetime.now()
print(datetime.now() - startTime)
"""
image details and abnormalitiy location.
1492_2 = 0
0145_2 = 1
1487_1 = 2
1527_1 = 3
"""

def get_details(val):
    if val == 0:
        image_path = "/home/a.cot12/Mam_dataset/dicom_M/1492-2.dcm"
        return [image_path, 1450, 1697, 1561, 1847]
    elif val == 1:
        image_path = "/home/a.cot12/Mam_dataset/dicom_M/0145-2.dcm"
        return [image_path, 1372, 1551, 1492, 1674]
    elif val == 2:
        image_path = "/home/a.cot12/Mam_dataset/dicom_M/1487-1.dcm"
        return [image_path, 214, 417, 1034, 1262]
    elif val == 3:
        image_path = "/home/a.cot12/Mam_dataset/dicom_M/1527-1.dcm"
        return [image_path, 514, 733, 1313, 1535]    
        
image_path, x1, x2, z1, z2 = get_details(2)
width = x2 - x1
height = z2 - z1
iterations = 10

LB = 0
t0 = 0
V0 = 1
alpha0 = 0.5
beta = 0.05 
LB = 0
batch_size = 10
scale = 100
image = UTILS.diread_area(image_path,x1,x2,z1,z2, LB)

binary_image = UTILS.IMAGE_THREASHOLD_OTSU(image)
threashold_image = UTILS.grow_region(image, binary_image)
dis = UTILS.estimate_distance(threashold_image, 200)
Vc = UTILS.threashold_volume(threashold_image)
time = UTILS.time_exponential_function(t0, V0, alpha0, Vc) + 2
walker_array = np.zeros((2, 1), dtype = np.int16)
scaled_time = (time * scale)
"""
Centre_start = UTILS.centre_start(threashold_image)
walker_array[:, 0] = [Centre_start[0], Centre_start[1]]
container_array = UTILS.inialise_2d_array(Centre_start[0],Centre_start[1], height, width)
"""
bright_start = np.argwhere(threashold_image.max() == threashold_image)
walker_array[:, 0] = [bright_start[0][0], bright_start[0][1]]
container_array = UTILS.inialise_2d_array(bright_start[0][0], bright_start[0][1], height, width)
output2 = "/home/a.cot12/modeling/1487_walkers_100_test/base_image_1487.png" 
output1 = "/home/a.cot12/modeling/1487_walkers_100_test/threashold_image_1487.png" 
plt.imsave(output2, image)
plt.imsave(output1, threashold_image , cmap = 'gray')



for t in range(0, scaled_time):
    epoch_time = t/scale
    GV = int(round(UTILS.exponential_function(epoch_time, t0, V0, alpha0),0))
    container_array, walker_array = UTILS.RUN_RANDOM_GROWTH(container_array, walker_array, threashold_image, height, width, GV, batch_size)
    if epoch_time == int(epoch_time):
        output = "/home/a.cot12/modeling/1487_walkers_100_test/%s.png" %(epoch_time)
        plt.imsave(output, container_array, cmap = 'gray')
	
    if (np.sum(container_array)/Vc) >= 0.99:
        break

output3 = "/home/a.cot12/modeling/1487_walkers_100_test/final.png" 


plt.imsave(output3, container_array, cmap = 'gray')
print(datetime.now() - startTime)

