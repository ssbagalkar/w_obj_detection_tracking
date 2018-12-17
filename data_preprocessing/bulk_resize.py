
import numpy as np
import cv2
import os

dir_path = '../../../vid.alegion.com/data/src/20181021/181016_55.254.1.19_4184test_12/frames'
out_path = '../../../vid.alegion.com/resize_raw'
if not os.path.isdir(out_path):
    os.mkdir(out_path)
num_of_images_resized=0
for filename in os.listdir(dir_path):
    print("Processing --> {}".format(filename))
    # If the images are not .png images, change the line below to match the image type.
    if filename.endswith(".png"):
        image = cv2.imread(os.path.join(dir_path,filename))
        print("Original Image size --> {}".format(image.shape))
        resized = cv2.resize(image,None,fx=0.125, fy=0.125, interpolation=cv2.INTER_AREA)
        print("Resizing successfull !!")
        print("Resizing will be stored to {}".format(os.path.join(out_path,filename)))
        cv2.imwrite(os.path.join(out_path,filename),resized)
        print("Resized image successfully written !!")
        print("Resized size --> {}".format(resized.shape))
        num_of_images_resized+=1
        print("---------------------------------")
        print("\n")

    else:
        print("Does not end in png")
        

print("Number of images sucessfully resized --> {}".format(num_of_images_resized))


