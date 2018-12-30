
import os
import pandas as pd
import numpy as np
import glob


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    all_cases = os.listdir(path_to_dir)
    all_case_locations = [os.path.join(path_to_dir,case) for case in all_cases ]
    csv_files=[]
    for case in all_case_locations:
        for filename in os.listdir(case):
            if filename.endswith(suffix):
                csv_files.append(os.path.join(path_to_dir,case,filename))
    return csv_files

    # return [ filename for filename in all_case_locations if filename.endswith( suffix ) ]



def split_into_train_test(input_dir, output_dir):
    if os.path.isdir(output_dir):
        print("Train and Test folders already present. Skipping.......")
        return -1

    if not os.path.isdir(input_dir):
        print("Input directory--> {} is not valid.".format(input_dir))
        return -1

    else:
        print("Input directory is present")
        print("Creating one csv by aggregating all csv's...")

        csv_filenames = find_csv_filenames(input_dir)
        print("Creating one pandas dataframe for all the csv files...")
        combined_csv = pd.concat([pd.read_csv(csv_files) for csv_files in csv_filenames ])
        df = pd.read_csv(combined_csv)
        filenames = list(set(list(['filename'].values)))
        print("Input directory has {} unique labels".format(len(filenames)))
        filenames.sort()
        np.random.seed(230)
        print("Shuffling dataset")
        np.random.shuffle(filenames)
        print("Perform train {}%  and test {}% split".format(int(85), int(15)))
        split = int(0.85 * len(filenames))
        train_filenames = filenames[:split]
        test_filenames = filenames[split:]
        print("Length of train set --> {}".format(len(train_filenames)))
        print("Length of test set --> {}".format(len(test_filenames)))

        if not os.path.isdir(output_dir):
            print("Output dir not present..creating it")
            os.makedirs(output_dir)

        # # Start reading the csv files to copy each row of associated filename to train and test accordingly
        # generate_train_test_csv(input_dir, output_dir, train_filenames, test_filenames, resized, resize_factor)
        #
        # generate_train_test_img_folders(input_dir, output_dir, train_filenames, test_filenames, resized, resize_factor)


