
import cv2
import os
import csv
import pandas as pd

def resize_files_and_annotations(image_dir=None,out_dir = None,resize_in_place=False, csv_file = None, scale_factor_x=8,scale_factor_y=8):
    if image_dir is None:
        print("Please specify an input image directory")
        return -1

    if resize_in_place and out_dir is None:
        print("Please specify an output image directory")
        return -1

    num_of_images_resized=0
    print("\t")
    print("Resizing files and labels...")
    for filename in os.listdir(os.path.join(image_dir,'data')):
        print("Processing --> {}".format(filename))
        # If the images are not .png images, change the line below to match the image type.
        if filename.endswith(".png"):
            image = cv2.imread(os.path.join(image_dir,'data',filename))
            print("Original Image size --> {}".format(image.shape))
            resized = cv2.resize(image,None,fx=scale_factor_x, fy=scale_factor_y, interpolation=cv2.INTER_AREA)
            print("Resizing successful!!")
            print("Resizing will be stored to {}".format(os.path.join(image_dir,'data',filename)))
            cv2.imwrite(os.path.join(image_dir,'data',filename),resized)
            print("Resized image successfully written !!")
            print("Resized size --> {}".format(resized.shape))
            num_of_images_resized+=1
            print("---------------------------------")
            print("\n")
        else:
            print("Does not end in png")
    print("Number of images successfully resized --> {}".format(num_of_images_resized))

    if not os.path.isfile(os.path.join(image_dir,'labels',csv_file)):
        print("CSV file not present. Cannot resize annotations...")
        return -1

    df = pd.read_csv(os.path.join(image_dir,'labels',csv_file))
    print("Resizing {} csv...".format(image_dir.split("\\")[-1]))
    df.loc[:,"width"] = df.loc[:,"width"]//8
    df.loc[:, "height"] = df.loc[:, "height"] // 8
    df.loc[:, "xmin"] = df.loc[:, "xmin"] // 8
    df.loc[:, "ymin"] = df.loc[:, "ymin"] // 8
    df.loc[:, "xmax"] = df.loc[:, "xmax"] // 8
    df.loc[:, "ymax"] = df.loc[:, "ymax"] // 8
    df.to_csv(os.path.join(image_dir,'labels',csv_file),index=None)


    print("Number of csv annotations sucessfully resized --> {}".format(len(df.index)))



