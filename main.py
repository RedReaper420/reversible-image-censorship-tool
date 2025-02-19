import numpy as np
from PIL import Image

import modules.data as data
import modules.hider as hider
import modules.mixer as mixer
import modules.noiser as noiser

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
    
    print("Enter the region to censor: Xpos Ypos Xsize Ysize")
    pos_x, pos_y, size_x, size_y = map(int, input().split())
    
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

input("\nPress enter to exit.")