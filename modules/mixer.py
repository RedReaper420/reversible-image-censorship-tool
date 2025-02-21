import numpy as np

MIX_NUM = 6

def censor(img_array, pos_x, pos_y, size_x, size_y):
    for mixes in range(MIX_NUM):
        region = np.array(img_array[pos_y:(pos_y + size_y), pos_x:(pos_x + size_x)])
        for row in range(size_x):
            for col in range(size_y):
                if size_x <= size_y:
                    index = col * size_x + row
                    new_col = index % size_y
                    new_row = index // size_y
                else:
                    index = col + row * size_y
                    new_col = index // size_x
                    new_row = index % size_x
                img_array[col + pos_y, row + pos_x] = region[new_col, new_row]
    
    return img_array

def uncensor(img_array, pos_x, pos_y, size_x, size_y, scale=1):
    pos_x *= scale
    pos_y *= scale
    size_x *= scale
    size_y *= scale
    
    for demixes in range(MIX_NUM):
        region = np.array(img_array[pos_y:(pos_y + size_y), pos_x:(pos_x + size_x)])
        for row in range(size_x):
            for col in range(size_y):
                if size_x <= size_y:
                    index = (col // scale) + (row // scale) * (size_y // scale)
                    new_col = index // (size_x // scale)
                    new_row = index % (size_x // scale)
                else:
                    index = (col // scale) * (size_x // scale) + (row // scale)
                    new_col = index % (size_y // scale)
                    new_row = index // (size_y // scale)
                img_array[col + pos_y, row + pos_x] = region[new_col * scale, new_row * scale]
    
    return img_array
