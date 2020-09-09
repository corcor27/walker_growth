import numpy as np
import pydicom as dicom
import walker_utilities as UTILS
import matplotlib.pyplot as plt
import random

              
def RUN_RANDOM_GROWTH(container_array, walker_array, threashold_array, height, width, GV):
    
    
    CV = np.sum(container_array)
    RW = int(GV - (CV + walker_array.shape[1]))
    if RW <= 0:
        for walker in range(0, walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, threashold_array)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x  
                container_array[new_z, new_x] += 1
            else:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x
                if threashold_array[walker_array[new_z, new_x] == 0:
                     ran_val = random.randint(0,walker_array.shape[1]-1)
                     walker_array = walker_array[:, ran_val]
            
                
    else:
                
        new_walkers = UTILS.new_growth_position_2(container_array, GV, walker_array)
        walker_array = np.append(walker_array, new_walkers,1)
        
        for walker in range(0,walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, threashold_array)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x 
                container_array[new_z, new_x] += 1
            else:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x
            
    
            
    return container_array, walker_array


    
    
    
