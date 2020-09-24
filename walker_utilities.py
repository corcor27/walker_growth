import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import gaussian_filter
from datetime import datetime
import random

def RUN_RANDOM_GROWTH(container_array, walker_array, threashold_array, height, width, GV, batch_size):
    
    
    CV = np.sum(container_array)
    RW = int(GV - (CV + walker_array.shape[1]))
    if RW <= 0:
        for walker in range(0, walker_array.shape[1]):
            new_z, new_x  = generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = random_availability_check(new_z,new_x, container_array, threashold_array)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x  
                container_array[new_z, new_x] += 1
            
                
                
    else:
        
        container_array, walker_array = brightest_growth(threashold_array, container_array, batch_size, RW, walker_array)
        for walker in range(0,walker_array.shape[1]):
            new_z, new_x  = generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = random_availability_check(new_z,new_x, container_array, threashold_array)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x 
                container_array[new_z, new_x] += 1
            
            
    
            
    return container_array, walker_array

def IMAGE_THREASHOLD_OTSU(image):
    output = "/home/a.cot12/modeling/0145_walkers_200/threashold.png"
    blur_image = gaussian_filter(image, sigma=5)
    plt.imsave(output, blur_image)
    img = cv2.imread(output, 0)
    ret,thr = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    threas_img = np.zeros((thr.shape))
    for kk in range(0, thr.shape[0]):
        for ii in range(0, thr.shape[1]):
            if thr[kk,ii] > 1:
                threas_img[kk,ii] = image[kk,ii]
    return threas_img

def generate_random_move(base_z, base_x):
    x = random.randint(-1,1)
    z = random.randint(-1,1)
    new_x, new_z = int(base_x + x), int(base_z + z)
    return new_z, new_x

    
def new_growth_position_2(container_array, req_num, walker_array):
    new_walker_array = np.zeros((2, req_num), dtype=np.int16)
    if walker_array.shape[1] == 1:
        for num in range(0, req_num):
            new_walker_array[:,num] = walker_array[:,0]
            
    else:
        for num in range(0, req_num):
            random_vals = np.random.randint(0, walker_array.shape[1]-1, req_num)
            new_walker_array[:,num] = walker_array[:,random_vals[num]]
    return new_walker_array      


def random_availability_check(zpos, xpos, container_array, template):
    if container_array[zpos,xpos] < template[zpos, xpos]:
        return 1
    else:
        return 0

        
def exponential_function(time, t0, V0, alpha0):
    time = time - t0
    V = V0*np.exp(time*alpha0)
    return V

def time_exponential_function(t0, V0, alpha, Vc):
    for time in range(0, 100000):
        time = time - t0
        V = V0*np.exp(time*alpha)
        if V >= Vc:
            return time
        

        
def inialise_2d_array(Z_start, X_start, hieght, width):
    container_array = np.zeros((hieght,width))
    container_array[Z_start, X_start] +=1
    return container_array


def centre_start(threashold_image):
    X_list = []
    Y_list = []
    for kk in range(0, threashold_image.shape[0]):
        for ii in range(0, threashold_image.shape[1]):
            if threashold_image[kk,ii] >= 1:
                X_list.append(ii)
                Y_list.append(kk)
    Xc = int(round(np.mean(X_list),0))
    Yc = int(round(np.mean(Y_list),))
    return Yc, Xc

def diread_area(path,x1,x2,z1,z2,LB):
    Beginning_image = dicom.dcmread(path)
    beginning_image = Beginning_image.pixel_array
    x1ml = x1
    x2ml = x2
    z1ml = z1
    z2ml = z2 
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

def threashold_volume(threashold_image):
    area = np.sum(threashold_image)
    return area





def patch(image, x,z):
    xlist = []
    zlist = []
    for kk in range(-1,2):
        for ii in range(-1,2):
            z_new = z + kk
            x_new = x + ii
            if image[z_new,x_new] > 0:
                zlist.append(z_new)
                xlist.append(x_new)
                
    return zlist, xlist

def bounds(z,x, image):
    if image[z,x] == 0:
        return 0
    else:
        return 1
    
def grow_region(image, threashold_image):
    Centre_start = centre_start(threashold_image)
    container = np.zeros((image.shape))
    listx = []
    listz = []
    listx.append(Centre_start[1])
    listz.append(Centre_start[0])
    while len(listx) > 0:
        x = listx[0]
        z = listz[0]
        Patch = patch(image, x,z)
        for rr in range(0, len(Patch[0])):
            if 2 <= Patch[0][rr] <= image.shape[0]-2 and 2 <= Patch[1][rr] <= image.shape[1] - 2:
                if threashold_image[Patch[0][rr], Patch[1][rr]] > 0 and container[Patch[0][rr], Patch[1][rr]] == 0:
                    container[Patch[0][rr], Patch[1][rr]] = 1
                    listx.append(Patch[1][rr])
                    listz.append(Patch[0][rr])
        listx.pop(0)
        listz.pop(0)
    for kk in range(2, image.shape[0]-2):
        for ii in range(2, image.shape[1]-2):
            if container[kk,ii] == 0:
                threashold_image[kk,ii] = 0
                
    return threashold_image
    
def estimate_distance(threashold_image, N):
    Centre_start = centre_start(threashold_image)
    distance = []
    for walker in range(0, N):
        walker_array = np.zeros((2, 1))
        val = 0
        while val < 1:
            addition_array = np.zeros((2, 1))
            walker_array[:,0] = Centre_start
            new_z, new_x  = generate_random_move(walker_array[0, -1], walker_array[1, -1])
            bound_val = bounds(new_z, new_x, threashold_image)
            if bound_val == 1:
                addition_array[:,0] = new_z, new_x
                walker_array = np.concatenate((walker_array, addition_array), axis=1)
            else:
                addition_array[:,0] = new_z, new_x
                walker_array = np.concatenate((walker_array, addition_array), axis=1)
                val = 1
                distance.append(walker_array.shape[1])
    mean_distance = int(round(sum(distance)/ len(distance), 0))
    print(distance[0])
    return mean_distance
        
    
def possible_pos_array(threashold_image, container_array):
    positions_array = np.zeros((threashold_image.shape))
    for kk in range(2, threashold_image.shape[0]-2):
        for ii in range(2, threashold_image.shape[1]-2):
            if threashold_image[kk,ii] > container_array[kk,ii]:
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        y, x = kk + dy, ii + dx
                        positions_array[y,x] = threashold_image[y,x] - container_array[y,x]
    return positions_array

def brightness_list(possible_positions, batch_size, container_array):
    walker_array = np.zeros((2, batch_size))
    for gg in range(0, batch_size):
        pos = np.argwhere(possible_positions.max() == possible_positions)
        possible_positions[pos[0][0],pos[0][1]] = 0
        container_array[pos[0][0],pos[0][1]] += 1
        walker_array[:,gg] = pos[0][0],pos[0][1]
    return container_array, walker_array
        
        
    

def brightest_growth(threashold_image, container_array, batch_size, req_vol, walker_array):
    if req_vol <= batch_size:
        aval_pos = possible_pos_array(threashold_image, container_array)
        container_array, new_walker_array = brightness_list(aval_pos, req_vol, container_array)
        walker_array = np.append(walker_array, new_walker_array, 1)
    else:
        NOI = int(np.floor(req_vol/batch_size))
        remainder = req_vol - (NOI*batch_size)
        for val in range(0, NOI):
            aval_pos = possible_pos_array(threashold_image, container_array)
            container_array, new_walker_array = brightness_list(aval_pos, batch_size, container_array)
            walker_array = np.append(walker_array, new_walker_array, 1)
        aval_pos = possible_pos_array(threashold_image, container_array)
        container_array, new_walker_array = brightness_list(aval_pos, remainder, container_array)
        walker_array = np.append(walker_array, new_walker_array, 1)
    
    return container_array, walker_array
                
                
                
        
            
