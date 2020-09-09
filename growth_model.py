import numpy as np
import pydicom as dicom
import model_utilities as UTILS
import matplotlib.pyplot as plt


def RUN_GROWTH_MODEL(container_array, template, height, width, depth, growth_rate, pixel_limitier,iterations):
    container_array = container_array
    offspring_count = 0
    for itt in range(0,iterations):
        print(itt)
        for kk in range(1, height-1):
            for jj in range(1, depth-1):
                for ii in range(1, width-1):
                    if 1 < container_array[kk,ii,jj] < pixel_limitier:
                        possible_offsprings = int(container_array[kk,ii,jj])
                        number_offsprings = UTILS.number_offsprings(possible_offsprings,kk,ii,jj,template,pixel_limitier, container_array,growth_rate, depth)
                        offspring_count += number_offsprings
                        for num in range(0,number_offsprings-1):
                            NearestNieghour =  UTILS.nearest_positions(template, container_array, kk, ii, jj, depth, pixel_limitier)
                            if len(NearestNieghour[0]) > 0:
                                z_pos = NearestNieghour[0]
                                x_pos = NearestNieghour[1]
                                y_pos = NearestNieghour[2]
                                #Pixel_likelihood = NearestNieghour[3]
                                #probalility_list = UTILS.probablitity(Pixel_likelihood)
                                #list_position = UTILS.find_move_position(probalility_list)
                                list_position = UTILS.random_move_position(z_pos)
                                container_array[z_pos[list_position],x_pos[list_position],y_pos[list_position]] += 1
        new_container_array = container_array - np.ones((height,width, depth))
        visul = UTILS.visualise(new_container_array, height, width, depth)
        output = r"D:\Documents\modeling\145-2\random_move\%d_%d.png" %(itt, growth_rate)
        plt.imsave(output,visul)
    return container_array, offspring_count

def Delete_Walkers(walker_array, threashold_image):
    for walker in range(0, walker_array.shape[1]-1):
        if threashold_image[walker_array[0, walker], walker_array[1, walker]] == 0:
            walker_array = np.delete(walker_array, walker, 1)
    return walker_array
              
def RUN_RANDOM_GROWTH(container_array, template, walker_array, threashold_array, height, width, GV):
    
    walker_array = Delete_Walkers(walker_array, threashold_array)
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
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x  
            
                
    else:
                
        new_walkers = UTILS.new_growth_position_2(container_array, GV, walker_array)
        walker_array = np.append(walker_array, new_walkers,1)
        
        for walker in range(0,walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, template)
            if value == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x 
                container_array[new_z, new_x] += 1
            else:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x
            
    
            
    return container_array, walker_array

def RUN_PROB_GROWTH(container_array, template, walker_array, threashold_array, height, width, GV, start_z, start_x):
    container_array = container_array
    walker_array = walker_array
    CV = np.sum(container_array)
    MA = int(GV - CV)
    RW = int(GV - (CV + walker_array.shape[1]))
    NW = walker_array.shape[1]
    print(MA, RW, NW)
    if RW <= 0:
        for walker in range(0, walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, template)
            move_chance = UTILS.probablity(template, container_array, new_z, new_x)
            if value == 1 and move_chance == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x  
                container_array[new_z, new_x] += 1
            else:
                walker_array[2, walker] += 1
                
    else:
                
        new_walkers = UTILS.new_growth_position_2(container_array, GV, walker_array)
        walker_array = np.append(walker_array, new_walkers,1)
        for walker in range(0,walker_array.shape[1]):
            new_z, new_x  = UTILS.generate_random_move(walker_array[0, walker], walker_array[1, walker])
            value = UTILS.random_availability_check(new_z,new_x, container_array, template)
            move_chance = UTILS.probablity(template, container_array, new_z, new_x)
            if value == 1 and move_chance == 1:
                walker_array[0, walker],walker_array[1, walker]  = new_z, new_x 
                container_array[new_z, new_x] += 1
            
            else: 
                walker_array[2, walker] += 1
                
    #walker_array = UTILS.Discrimate_walkers(walker_array)
    
            
    return container_array, walker_array    

"""   
    if len(failed) > 0:
        for ii in range(0, len(failed)):
            val = UTILS.pick_new_location(walker_array, failed)
            x, z = walker_array[:, val]
            new_positions = UTILS.growth_help(x, z)
            walker_array[0,ii] = int(new_positions[0])
            walker_array[1,ii] = int(new_positions[1])
            check_value = UTILS.random_availability_check(int(new_positions[1]), int(new_positions[0]), container_array, template)
            if check_value == 1:
                container_array[int(new_positions[1]), int(new_positions[0])] += 1 
            else:
                val = UTILS.pick_new_location(walker_array, failed)
            
                x, z = walker_array[:, val]
                new_positions = UTILS.generate_random_move(x, z)
                walker_array[0,ii] = int(new_positions[0])
                walker_array[1,ii] = int(new_positions[1])
                check_value = UTILS.random_availability_check(int(new_positions[1]), int(new_positions[0]), container_array, template)
                if check_value == 1:
                    container_array[int(new_positions[1]), int(new_positions[0])] += 1
"""
    
            
    
    
    
