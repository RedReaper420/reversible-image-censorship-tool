import numpy as np

def noise(channel_value, col, row, sign=1, scale=1):
    channel_value = int(channel_value)
    seed = (col // scale + 63) * (row // scale + 1) * 71
    out_value = (channel_value + seed * sign) % 256
    
    return out_value

def censor(img_array, pos_x, pos_y, size_x, size_y):
    for row in range(size_x):
        for col in range(size_y):
            # Noising
            img_array[col + pos_y, row + pos_x][0] = noise(img_array[col + pos_y, row + pos_x][0], col, row)
            img_array[col + pos_y, row + pos_x][1] = noise(img_array[col + pos_y, row + pos_x][1], col, row)
            img_array[col + pos_y, row + pos_x][2] = noise(img_array[col + pos_y, row + pos_x][2], col, row)
            
            # Hue shifting
            img_array[col + pos_y, row + pos_x][0], \
            img_array[col + pos_y, row + pos_x][1], \
            img_array[col + pos_y, row + pos_x][2] = \
            img_array[col + pos_y, row + pos_x][1], \
            img_array[col + pos_y, row + pos_x][2], \
            img_array[col + pos_y, row + pos_x][0]
    
    return img_array

def uncensor(img_array, pos_x, pos_y, size_x, size_y, scale):
    pos_x *= scale
    pos_y *= scale
    size_x *= scale
    size_y *= scale
    
    for row in range(size_x):
        for col in range(size_y):
            # Denoising
            img_array[col + pos_y, row + pos_x][0] = noise(img_array[col + pos_y, row + pos_x][0], col, row, -1, scale)
            img_array[col + pos_y, row + pos_x][1] = noise(img_array[col + pos_y, row + pos_x][1], col, row, -1, scale)
            img_array[col + pos_y, row + pos_x][2] = noise(img_array[col + pos_y, row + pos_x][2], col, row, -1, scale)
            
            # Reverting hue shifting
            img_array[col + pos_y, row + pos_x][0], \
            img_array[col + pos_y, row + pos_x][1], \
            img_array[col + pos_y, row + pos_x][2] = \
            img_array[col + pos_y, row + pos_x][2], \
            img_array[col + pos_y, row + pos_x][0], \
            img_array[col + pos_y, row + pos_x][1]
    
    return img_array
