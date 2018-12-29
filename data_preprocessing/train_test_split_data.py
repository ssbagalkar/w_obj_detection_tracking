
import os
import pandas as pd
import numpy as np

def split_into_train_test(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print("Input directory--> {} is not valid.".format(input_dir))
        return -1
    else:
        print("Input directory is present")
        print("Creating one csv by aggregating all csv's...")

        combined_csv = pd.concat([pd.read_csv(csv_files) for csv_files in input_dir if csv_files.endswith(".csv") ])
        print("Creating one pandas dataframe for all the csv files...")

        df = pd.read_csv(input_dir)
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


