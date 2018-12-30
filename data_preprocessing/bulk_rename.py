# Rename the image files and all their annotations
import os
def rename_files(image_dir):

    print("Started to rename files...")
    rename_index_total = 0

    print("Root image directory is {}".format(image_dir))
    print("Root directory has {} children folders with annotations and frames folders for each".format(len([name for name in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir,name))])))
    print("\t\t")

    for dir in os.listdir(image_dir):

        print("-------------------------------------------------------------------")
        print("Processing ---->  {}".format(dir))
        rename_index_cases = 0
        rename_index_files = 0
        rename_index_xmls = 0
        for child_folder in os.listdir(os.path.join(image_dir + "\\" + dir)):
            if not os.path.isdir(os.path.join(image_dir, dir, child_folder)):
                continue

            for img_file in os.listdir(os.path.join(image_dir, dir, child_folder)):
                if(img_file.split(".")[1] == "xml"):
                    if not img_file.startswith(dir):
                        os.rename(os.path.join(image_dir,dir,child_folder,img_file), image_dir+"\\"+dir+"\\"+child_folder+"\\"+dir+"_"+img_file)
                        rename_index_xmls+=1
                    else:
                        print("XML file already renamed")
                elif (img_file.split(".")[1] == "png"):
                    if not img_file.startswith(dir):
                        os.rename(os.path.join(image_dir, dir, child_folder, img_file),image_dir + "\\" + dir + "\\" + child_folder + "\\" + dir + "_" + img_file)
                        rename_index_files += 1
                    else:
                        print("Image file already renamed")

            if child_folder == "annotations":
                print("----Renamed--> {} files in dir--> {}".format(rename_index_xmls,child_folder))
            elif child_folder == "frames":
                print("----Renamed--> {} files in dir--> {}".format(rename_index_files, child_folder))

        if rename_index_xmls != 0 and rename_index_files != 0:
            rename_index_cases += 2
            rename_index_total += 1
            print("Renamed {} folders and {} files in dir--> {}".format(rename_index_cases,
                                                                        rename_index_files + rename_index_xmls, dir))
        else:
            print("All files already renamed in dir--> {}".format(dir))


        print("-------------------------------------------------------------------")
        print("\t\t\t")




    print("Total Folders processed--> {}".format(rename_index_total))


#
# rename_files("C:\\Users\\saurabh\\Documents\\code\\raw_data\\data")
