import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import walker_utilities as UTILS
import cv2
from scipy.ndimage import gaussian_filter
from datetime import datetime
import pandas as pd
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
        
image_path, x1, x2, z1, z2 = get_details(1)
width = x2 - x1 + 150
height = z2 - z1 + 150
iterations = 10

LB = 0
t0 = 0
V0 = 1
alpha0 = 0.5
beta = 0.05 
LB = 0
batch_size = 10
scale = 25
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
#output2 = "/home/a.cot12/modeling/0145_walkers_100/base_image_0145.png" 
#output1 = "/home/a.cot12/modeling/0145_walkers_100/threashold_image_0145.png" 
#plt.imsave(output2, image)
#plt.imsave(output1, threashold_image , cmap = 'gray')
time_array = []
volume_array = []


for t in range(0, scaled_time):
    epoch_time = t/scale
    GV = int(round(UTILS.exponential_function(epoch_time, t0, V0, alpha0),0))
    container_array, walker_array = UTILS.RUN_RANDOM_GROWTH(container_array, walker_array, threashold_image, height, width, GV, batch_size)
    time_array.append(epoch_time)
    volume_array.append(np.sum(container_array))
    if (np.sum(container_array)/Vc) >= 0.99:
        break

		#if epoch_time == int(epoch_time):
			#output = "/home/a.cot12/modeling/0145_walkers_100/%s.png" %(epoch_time)
			#plt.imsave(output, container_array, cmap = 'gray')

    
	
	
df = pd.DataFrame(list(zip(time_array,volume_array)), columns = ['Time','Volume'])
output = "/home/a.cot12/modeling/0145_walkers_25/volume.csv" 
df.to_csv(output)    
#output3 = "/home/a.cot12/modeling/0145_walkers_100/final.png" 


#plt.imsave(output3, container_array, cmap = 'gray')
#print(datetime.now() - startTime)

