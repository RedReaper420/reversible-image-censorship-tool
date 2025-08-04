import numpy as np

# This transformation method subtracts the value of one pixel by the value of its previous pixel. A checker pattern is applied, subtraction is being applied by columns and by rows.

def censor(img_array, pos_x, pos_y, size_x, size_y):
    for row in range(size_y):
        for col in range(size_x):
            for channel in range(3):
                shift = row % 2
                
                if col == 0:
                    neighbor_value = 0
                else:
                    neighbor_value = int(img_array[pos_y + row, pos_x + col - 1 + shift][channel])
                current_value = int(img_array[pos_y + row, pos_x + col + shift][channel])
                
                img_array[pos_y + row, pos_x + col + shift][channel] = (current_value - neighbor_value) % 256
    
    for row in range(size_y):
        for col in range(size_x):
            for channel in range(3):
                shift = (col + 1) % 2
                
                if row == 0:
                    neighbor_value = 0
                else:
                    neighbor_value = int(img_array[pos_y + row - 1 + shift, pos_x + col][channel])
                current_value = int(img_array[pos_y + row + shift, pos_x + col][channel])
                
                img_array[pos_y + row + shift, pos_x + col][channel] = (current_value - neighbor_value) % 256
    
    return img_array

def uncensor(img_array, pos_x, pos_y, size_x, size_y, scale):
    pos_x *= scale
    pos_y *= scale
    size_x *= scale
    size_y *= scale
    
    for row in reversed(range(size_y)):
        for col in range(size_x):
            for channel in range(3):
                shift = ((col // scale + 1) % 2) * scale
                
                if row // scale == 0:
                    neighbor_value = 0
                else:
                    neighbor_value = int(img_array[pos_y + row - 1*scale + shift, pos_x + col][channel])
                current_value = int(img_array[pos_y + row + shift, pos_x + col][channel])
                
                img_array[pos_y + row + shift, pos_x + col][channel] = (current_value + neighbor_value) % 256
    
    for row in range(size_y):
        for col in reversed(range(size_x)):
            for channel in range(3):
                shift = (row // scale % 2) * scale
                
                if col // scale == 0:
                    neighbor_value = 0
                else:
                    neighbor_value = int(img_array[pos_y + row, pos_x + col - 1*scale + shift][channel])
                current_value = int(img_array[pos_y + row, pos_x + col + shift][channel])
                
                img_array[pos_y + row, pos_x + col + shift][channel] = (current_value + neighbor_value) % 256
    
    return img_array
