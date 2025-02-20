import numpy as np
from PIL import Image

import modules.data as data
import modules.hider as hider
import modules.mixer as mixer
import modules.noiser as noiser

WORD = 16

def main():
    correct = False
    while correct == False:
        mode = input("Select the mode: 1 - Uncensor, 2 - Censor\n")
        if mode == "1" or mode == "2":
            correct = True

    if mode == "1":
        # Uncensoring
        
        print("Loading the censored image.")
        with Image.open("censored.png") as input_img:
            input_img.load()
        input_img = input_img.convert("RGBA")
        img_array = np.array(input_img)
        print("Loaded.\n")
        
        print("Exctracting uncensoring data.")
        image_data = data.extract(img_array)
        
        img_array = image_data[0]
        pos_x = image_data[1]
        pos_y = image_data[2]
        size_x = image_data[3]
        size_y = image_data[4]
        scale = image_data[5]
        methods = image_data[6]
        
        print("Uncensoring.")
        if methods[2] == 1:
            print("Unhiding...")
            img_array = hider.uncensor(img_array, pos_x, pos_y, size_x, size_y, scale)
        if methods[1] == 1:
            print("Denoising...")
            img_array = noiser.uncensor(img_array, pos_x, pos_y, size_x, size_y, scale)
        if methods[0] == 1:
            print("Unmixing...")
            img_array = mixer.uncensor(img_array, pos_x, pos_y, size_x, size_y, scale)
        
        output_img = Image.fromarray(img_array)
        output_img.save("uncensored.png")
        print("Image uncensored.")
        
    else:
        # Censoring
        
        print("Loading the original image.")
        with Image.open("original.png") as input_img:
            input_img.load()
        input_img = input_img.convert("RGBA")
        img_array = np.array(input_img)
        print("Loaded.\n")
        
        regions_num_max = (input_img.size[0] - 2) // (WORD * 4)
        if regions_num_max == 0:
            print("The image must be at least 66 pixels wide to be censored.")
            return
        regions = [[0, 0, 0, 0] * regions_num_max]
        print("This image may contain up to " + str(regions_num_max) + " censored region(s).")
        
        if regions_num_max > 1:
            regions_num = int(input("Specify the number of regions to input: "))
            if regions_num <= 0:
                print("Regions number must be greater than 0. Reassigned the number to 1.")
                regions_num = 1
            elif regions_num > regions_num_max:
                print("Regions number must not be greater than {0}. Reassigned the number to {0}.".format(regions_num_max))
                regions_num = regions_num_max
        else:
            regions_num = 1 # No specification needed if there is just 1 region available.
        print()
        
        print("Enter the region(s) to censor: Xpos Ypos Xsize Ysize")
        for i in range(regions_num):
            pos_x, pos_y, size_x, size_y = map(int, input("{0}/{1}: ".format(i + 1, regions_num)).split())
            regions[i][0] = pos_x
            regions[i][1] = pos_y
            regions[i][2] = size_x
            regions[i][3] = size_y
        
        print("\nSelect the censoring methods: Mixing Noising Hiding")
        print("Input 3 flags (1s or 0s): ")
        flag_mixing, flag_noising, flag_hiding = map(int, input().split())
        methods = [flag_mixing, flag_noising, flag_hiding]
        
        print("\nCensoring the image.")
        if flag_mixing == 1:
            print("Mixing...")
            img_array = mixer.censor(img_array, pos_x, pos_y, size_x, size_y)
        if flag_noising == 1:
            print("Noising...")
            img_array = noiser.censor(img_array, pos_x, pos_y, size_x, size_y)
        if flag_hiding == 1:
            print("Hiding...")
            img_array = hider.censor(img_array, pos_x, pos_y, size_x, size_y)
        print("Injecting data for uncensoring.")
        img_array = data.inject(img_array, pos_x, pos_y, size_x, size_y, methods)
        
        output_img = Image.fromarray(img_array)
        output_img.save("censored.png")
        print("Image censored.")

main()
input("\nPress enter to exit.")