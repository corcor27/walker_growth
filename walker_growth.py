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
def RUN_RANDOM_GROWTH(container_array, template, walker_array, threashold_array, height, width, GV):
    container_array = container_array
    walker_array = walker_array
    CV = np.sum(container_array)
    RW = int(GV - (CV + walker_array.shape[1]))
    if RW <= 0:
        for walker in range(0, walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, template)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x  
                container_array[new_z, new_x] += 1
            
                
    else:
                
        new_walkers = UTILS.new_growth_position_2(container_array, GV, walker_array)
        walker_array = np.append(walker_array, new_walkers,1)
        for walker in range(0,walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, template)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x 
                container_array[new_z, new_x] += 1
                
def diread_area(path,x1,x2,z1,z2,LB):
    Beginning_image = dicom.dcmread(path)
    beginning_image = Beginning_image.pixel_array
    x1ml = x1 - 75
    x2ml = x2 + 75
    z1ml = z1 - 75
    z2ml = z2 + 75
    diffxml = x2ml - x1ml
    diffzml = z2ml - z1ml
    array = np.zeros((diffzml, diffxml))
    for j in range(z1ml, z2ml):
        for k in range(x1ml, x2ml):
            array[j-z1ml,k-x1ml] = beginning_image[j,k]
    density = np.zeros((diffzml,diffxml),dtype = int)
    UB = np.amax(array)
    for i in range(0, diffzml):
        for j in range(0, diffxml):
            lum = array[i,j]
            if LB <= lum <= UB:
                density[i,j] = lum
            else:
                density[i,j] = 0
    return density


image_path = r"C:\Users\cory1\Documents\test-folder\data_set\Malignant\dicom_M\1492-2.dcm"

x1 = 1450
x2 = 1697
z1 = 1561
z2 = 1847
width = x2 - x1 + 150
height = z2 - z1 + 150
iterations = 10

LB = 0
t0 = 0
V0 = 1
alpha0 = 0.5
beta = 0.05 
LB = 0
image = diread_area(image_path,x1,x2,z1,z2, LB)

binary_image = UTILS.IMAGE_THREASHOLD_OTSU(image)
threashold_image = REGION.grow_region(image, binary_image)
template = threashold_image
dis = REGION.estimate_distance(threashold_image, 200)


Vc = IMREAD.threashold_volume(threashold_image)
time = UTILS.time_exponential_function(t0, V0, alpha0, Vc)
scale= int(round(dis/time))
delay_start = 18 * scale
scaled_time = (time * scale)
walker_array = np.zeros((2, 1), dtype = np.int16)

Centre_start = UTILS.Centre_start(threashold_image)
walker_array[:, 0] = [Centre_start[0], Centre_start[1]]
container_array = UTILS.inialise_2d_array(Centre_start[0],Centre_start[1], height, width)
Centre_start = UTILS.Centre_start(threashold_image)
print(scaled_time)

for t in range(delay_start, scaled_time):
    epoch_time = t/scale
    print(epoch_time)
    GV = int(round(UTILS.exponential_function(epoch_time, t0, V0, alpha0),0))
    new_container_array = RUN_RANDOM_GROWTH(container_array, template, walker_array, threashold_image[0], height, width, GV)
    walker_array = new_container_array[1]
    container_array = new_container_array[0]
    if epoch_time == int(epoch_time):
        visul = container_array
        output = r"D:\Documents\modeling\model_test7\%s.png" %(epoch_time)
        amount_left = (np.sum(container_array)/ Vc)
        print(amount_left)
        plt.imsave(output, visul, cmap = 'gray')

output = r"D:\Documents\modeling\model_test7\final.png" 
output1 = r"D:\Documents\modeling\model_test7\threashold_image_1492-2.png" 
output2 = r"D:\Documents\modeling\model_test7\base_image_1492-2.png" 
plt.imsave(output, container_array, cmap = 'gray')
plt.imsave(output1, threashold_image , cmap = 'gray')
plt.imsave(output2, image , cmap = 'gray')


plt.imshow(template)