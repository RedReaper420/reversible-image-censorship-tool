import numpy as np

# This transformation method generates a pseudo-random value according to the pixel position, and adds this value to the pixel, then performs modulo 256. Additionally, color channels are being swapped.

def noise(channel_value, col, row, sign=1, scale=1):
    channel_value = int(channel_value)
    seed = (col // scale + 63) * (row // scale + 1) * 71
    return (channel_value + seed * sign) % 256

def censor(img_array, pos_x, pos_y, size_x, size_y):
    for row in range(size_x):
        for col in range(size_y):
            # Noising
            for channel in range(3):
                img_array[col + pos_y, row + pos_x][channel] = noise(img_array[col + pos_y, row + pos_x][channel], col, row)
            
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
            for channel in range(3):
                img_array[col + pos_y, row + pos_x][channel] = noise(img_array[col + pos_y, row + pos_x][channel], col, row, -1, scale)
            
            # Reverting hue shifting
            img_array[col + pos_y, row + pos_x][0], \
            img_array[col + pos_y, row + pos_x][1], \
            img_array[col + pos_y, row + pos_x][2] = \
            img_array[col + pos_y, row + pos_x][2], \
            img_array[col + pos_y, row + pos_x][0], \
            img_array[col + pos_y, row + pos_x][1]
    
    return img_array
