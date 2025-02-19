import numpy as np
from PIL import Image

WORD = 16
METHODS_NUM = 3
 
def bit_write(channel_value, data_bit):
    sign = 1
    if channel_value == 255:
        sign = -1
    return channel_value + ((channel_value % 2) ^ data_bit) * sign

def bit_read(channel_value):
    return channel_value % 2

def to_bin(value):
    bin_value = bin(value)[2:]
    bin_value = "0" * (WORD - len(bin_value)) + bin_value
    return bin_value

def inject(img_array, pos_x, pos_y, size_x, size_y, methods):
    img_original = Image.fromarray(img_array)
    width, height = img_original.size
    
    # Adding an additional row
    height += 1
    img_resized = img_original.resize((width, height), Image.Resampling.NEAREST)
    img_resized.paste(img_original)
    img_array = np.array(img_resized)
    
    # Scale mark
    img_array[height-1, width-1 - 0][2] = bit_write(img_array[height-1, width-1 - 0][2], 0)
    img_array[height-1, width-1 - 1][2] = bit_write(img_array[height-1, width-1 - 1][2], 1)
    
    # Region coordinates and size conversion to binary
    bin_pos_x = to_bin(pos_x)
    bin_pos_y = to_bin(pos_y)
    bin_size_x = to_bin(size_x)
    bin_size_y = to_bin(size_y)
    
    # Region coordinates and size (binary) writing
    for i in range(WORD):
        img_array[height-1, width-1 - 2 - WORD*0 - i][2] = bit_write(img_array[height-1, width-1 - 2 - WORD*0 - i][2], int(bin_pos_x[-(i+1)]))
        img_array[height-1, width-1 - 2 - WORD*1 - i][2] = bit_write(img_array[height-1, width-1 - 2 - WORD*1 - i][2], int(bin_pos_y[-(i+1)]))
        img_array[height-1, width-1 - 2 - WORD*2 - i][2] = bit_write(img_array[height-1, width-1 - 2 - WORD*2 - i][2], int(bin_size_x[-(i+1)]))
        img_array[height-1, width-1 - 2 - WORD*3 - i][2] = bit_write(img_array[height-1, width-1 - 2 - WORD*3 - i][2], int(bin_size_y[-(i+1)]))
    
    # Methods flags writing
    for i in range(METHODS_NUM):
        img_array[height-1, width-1 - 2 - WORD*4 - i][2] = bit_write(img_array[height-1, width-1 - 2 - WORD*4 - i][2], methods[i])
    
    return img_array

def extract(img_array):
    img_original = Image.fromarray(img_array)
    width, height = img_original.size
    
    # Getting scale
    scale = 0
    mark = 0
    while mark == 0:
        mark = bit_read(img_array[height-1, width-1 - scale][2])
        if mark == 0:
            scale += 1
    
    # Reading region coordinates and size
    pos_x = 0
    pos_y = 0
    size_x = 0
    size_y = 0
    for i in range(WORD):
        pos_x += bit_read(img_array[height-1, width-1 - 2*scale - WORD*0*scale - i*scale][2]) * (2**i)
        pos_y += bit_read(img_array[height-1, width-1 - 2*scale - WORD*1*scale - i*scale][2]) * (2**i)
        size_x += bit_read(img_array[height-1, width-1 - 2*scale - WORD*2*scale - i*scale][2]) * (2**i)
        size_y += bit_read(img_array[height-1, width-1 - 2*scale - WORD*3*scale - i*scale][2]) * (2**i)
    
    # Reading methods flags
    methods = []
    for i in range(METHODS_NUM):
        methods.append(bit_read(img_array[height-1, width-1 - 2*scale - WORD*4*scale - i*scale][2]))
    
    # Deleting the last row
    img_resized = img_original.crop((0, 0, width, height - 1*scale))
    img_array = np.array(img_resized)
    
    return [img_array, pos_x, pos_y, size_x, size_y, scale, methods]
