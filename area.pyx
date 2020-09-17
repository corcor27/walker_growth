def possible_pos_array(threashold_image, container_array):
    @cython.boundscheck(False)  # turn off array bounds check
    @cython.wraparound(False)
    cdef int ymax = threashold_image.shape[0]
    cdef int xmax = threashold_image.shape[1]
    cdef int y,x
    cdef np.ndarray  positions_array = np.zeros([xmax, ymax], dtype=np.int)
    for kk in range(1, ymax-1):
        for ii in range(1, xmax-1):
            if threashold_image[kk,ii] > container_array[kk,ii]:
                for dy in range(-1,2):
                    for dx in range(-1,2):
                        y, x = kk + dy, ii + dx
                        positions_array[y,x] = threashold_image[y,x] - container_array[y,x]
    return positions_array
