import numpy as np

# This transformation method makes opaque pixels transparent, while saving the actual color data.

def censor(img_array, pos_x, pos_y, size_x, size_y):
    for row in range(size_x):
        for col in range(size_y):
            img_array[col + pos_y, row + pos_x][3] = 0
    
    return img_array

def uncensor(img_array, pos_x, pos_y, size_x, size_y, scale):
    pos_x *= scale
    pos_y *= scale
    size_x *= scale
    size_y *= scale
    
    for row in range(size_x):
        for col in range(size_y):
            img_array[col + pos_y, row + pos_x][3] = 255
    
    return img_array
