
import cv2
import os
import csv

def resize_files_and_annotations(image_dir=None,out_dir = None,csv_file_name=None,scale_factor_x = 0.125,scale_factor_y=0.125):
    if image_dir is None:
        print("Please specify an input image directory")
        return -1

    if out_dir is None:
        print("Please specify an output image directory")
        return -1

    num_of_images_resized=0
    for filename in os.listdir(os.path.join(image_dir)):
        print("Processing --> {}".format(filename))
        # If the images are not .png images, change the line below to match the image type.
        if filename.endswith(".png"):
            image = cv2.imread(os.path.join(image_dir,filename))
            print("Original Image size --> {}".format(image.shape))
            resized = cv2.resize(image,None,fx=scale_factor_x, fy=scale_factor_y, interpolation=cv2.INTER_AREA)
            print("Resizing successfull !!")
            print("Resizing will be stored to {}".format(os.path.join(image_dir,filename)))
            cv2.imwrite(os.path.join(image_dir,filename),resized)
            print("Resized image successfully written !!")
            print("Resized size --> {}".format(resized.shape))
            num_of_images_resized+=1
            print("---------------------------------")
            print("\n")
        else:
            print("Does not end in png")
    print("Number of images successfully resized --> {}".format(num_of_images_resized))

    if not os.path.isfile(os.path.join(image_dir,csv_file_name)):
        print("CSV file not present. Cannot resize annotations...")
        return -1

    with open(csv_file_name, mode='wb') as walmart_csv:
        csv_reader = csv.DictReader(walmart_csv)
        headers = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        csv_writer = csv.DictWriter(walmart_csv, fieldnames=headers)
        csv_line_count=0
        for row in csv_reader:
            if csv_line_count==0:
                csv_writer.writeheader()
            else:
                row["width"] = str(int(row["width"]) // scale_factor_x)
                row["height"] = str(int(row["height"]) // scale_factor_y)
                row["xmin"] = str(int(row["xmin"]) // scale_factor_x)
                row["ymin"] = str(int(row["ymin"]) // scale_factor_y)
                row["xmax"] = str(int(row["xmax"]) // scale_factor_x)
                row["ymax"] = int(int(row["ymax"]) // scale_factor_y)
                csv_writer.writerow(row)
            csv_line_count += 1



    print("Number of csv annotations sucessfully resized --> {}".format(csv_line_count))



