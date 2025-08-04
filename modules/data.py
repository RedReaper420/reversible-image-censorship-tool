import numpy as np
from PIL import Image

WORD = 16 # The support of images with sides sizes up to 65535 should be enough, right?
METHODS_NUM = 4 # Without the need to rewrite data positioning in the data row, there can be up to 4 methods.

def bit_write(channel_value, data_bit):
    sign = 1
    if channel_value == 255:
        sign = -1
    return channel_value + ((channel_value % 2) ^ data_bit) * sign

def bit_read(channel_value):
    return int(channel_value) % 2

def to_bin(value):
    bin_value = bin(value)[2:]
    bin_value = "0" * (WORD - len(bin_value)) + bin_value
    return bin_value

def inject(img_array, regions, methods):
    img_original = Image.fromarray(img_array)
    width, height = img_original.size
    regions_num = len(regions)
    
    # Adding an additional row
    height += 1
    img_resized = img_original.resize((width, height), Image.Resampling.NEAREST)
    img_resized.paste(img_original)
    img_array = np.array(img_resized)
    
    # Scale mark in the B channel
    img_array[height-1, width-1 - 0][2] = bit_write(img_array[height-1, width-1 - 0][2], 0)
    img_array[height-1, width-1 - 1][2] = bit_write(img_array[height-1, width-1 - 1][2], 1)
    
    for r in range(regions_num):
        # Region coordinates and size conversion to binary
        bin_pos_x = to_bin(regions[r][0])
        bin_pos_y = to_bin(regions[r][1])
        bin_size_x = to_bin(regions[r][2])
        bin_size_y = to_bin(regions[r][3])
        
        # Region coordinates and size (binary) writing
        for i in range(WORD):
            r_shift = (r // 3) * 4
            
            img_array[height-1, width-1 - 2 - WORD*(0+r_shift) - i][r % 3] = bit_write(\
            img_array[height-1, width-1 - 2 - WORD*(0+r_shift) - i][r % 3], int(bin_pos_x[-(i+1)]))
            
            img_array[height-1, width-1 - 2 - WORD*(1+r_shift) - i][r % 3] = bit_write(\
            img_array[height-1, width-1 - 2 - WORD*(1+r_shift) - i][r % 3], int(bin_pos_y[-(i+1)]))
            
            img_array[height-1, width-1 - 2 - WORD*(2+r_shift) - i][r % 3] = bit_write(\
            img_array[height-1, width-1 - 2 - WORD*(2+r_shift) - i][r % 3], int(bin_size_x[-(i+1)]))
            
            img_array[height-1, width-1 - 2 - WORD*(3+r_shift) - i][r % 3] = bit_write(\
            img_array[height-1, width-1 - 2 - WORD*(3+r_shift) - i][r % 3], int(bin_size_y[-(i+1)]))
    
    # Methods flags writing, in the first 2 pixels, in the R and G channels
    for i in range(METHODS_NUM):
        img_array[height-1, width-1 - i // 2][i % 2] = bit_write(\
        img_array[height-1, width-1 - i // 2][i % 2], methods[i])
    
    return img_array

def extract(img_array):
    img_original = Image.fromarray(img_array)
    width, height = img_original.size
    
    # Getting scale, from the first 2 original pixels, from the B channel
    scale = 0
    mark = 0
    while mark == 0:
        mark = bit_read(img_array[height-1, width-1 - scale][2])
        if mark == 0:
            scale += 1
    
    # Reading coordinates and size for each region
    regions_num = (width - 2*scale) // (WORD * 4 * scale) * 3
    regions = []
    for r in range(regions_num):
        regions.append([0, 0, 0, 0])
        pos_x = 0
        pos_y = 0
        size_x = 0
        size_y = 0
        
        for i in range(WORD):
            r_shift = (r // 3) * 4
            pos_x += bit_read(img_array[height-1, width-1 - (2 + WORD*(0+r_shift) + i)*scale][r % 3]) * (2**i)
            pos_y += bit_read(img_array[height-1, width-1 - (2 + WORD*(1+r_shift) + i)*scale][r % 3]) * (2**i)
            size_x += bit_read(img_array[height-1, width-1 - (2 + WORD*(2+r_shift) + i)*scale][r % 3]) * (2**i)
            size_y += bit_read(img_array[height-1, width-1 - (2 + WORD*(3+r_shift) + i)*scale][r % 3]) * (2**i)
        
        regions[r][0] = pos_x
        regions[r][1] = pos_y
        regions[r][2] = size_x
        regions[r][3] = size_y
    
    # Reading methods flags from the first 2 pixels, from the R and G channels
    methods = []
    for i in range(METHODS_NUM):
        methods.append(bit_read(img_array[height-1, width-1 - (i // 2)*scale][i % 2]))
    
    # Deleting the last row
    img_resized = img_original.crop((0, 0, width, height - 1*scale))
    img_array = np.array(img_resized)
    
    return [img_array, scale, methods, regions]
