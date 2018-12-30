
import os
import pandas as pd
import numpy as np
import csv


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


def generate_train_test_csv(train_filenames, test_filenames,train_test_dir ):

    # declare all paths
    original_csv_path = os.path.join(train_test_dir, 'walmart_labels.csv')
    print("Creating train folder...")
    os.makedirs(os.path.join(train_test_dir,'train'))
    print("Creating test folder...")
    os.makedirs(os.path.join(train_test_dir, 'test'))
    train_csv_path = os.path.join(train_test_dir,'train', 'train_labels.csv')
    test_csv_path = os.path.join(train_test_dir, 'test','test_labels.csv')

    with open(original_csv_path, mode='r') as csv_file_in, open(train_csv_path, mode='w',newline='') as csv_train, open(test_csv_path, mode='w', newline='') as csv_test:
        csv_reader = csv.DictReader(csv_file_in)
        #         first_row = next(csv_reader)
        headers = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        #         print(headers)
        print("Headers are {}".format(headers))
        csv_train_write = csv.DictWriter(csv_train, fieldnames=headers)
        csv_test_write = csv.DictWriter(csv_test, fieldnames=headers)
        csv_train_write.writeheader()
        csv_test_write.writeheader()
        print("Headers written for both files")
        line_count = 0
        num_lines_train = 0
        num_lines_test = 0
        for row in csv_reader:
            if row["filename"] in train_filenames:
                print("{}--> {} is in train_set".format(row["filename"], row["class"]))
                row["width"] = str(int(row["width"]))
                row["height"] = str(int(row["height"]))
                row["xmin"] = str(int(row["xmin"]))
                row["ymin"] = str(int(row["ymin"]))
                row["xmax"] = str(int(row["xmax"]))
                row["ymax"] = int(int(row["ymax"]))
                csv_train_write.writerow(row)
                num_lines_train += 1
            elif row["filename"] in test_filenames:
                print("{}--> {} is in test_set".format(row["filename"], row["class"]))
                row["width"] = str(int(row["width"]))
                row["height"] = str(int(row["height"]))
                row["xmin"] = str(int(row["xmin"]))
                row["ymin"] = str(int(row["ymin"]))
                row["xmax"] = str(int(row["xmax"]))
                row["ymax"] = int(int(row["ymax"]))
                csv_test_write.writerow(row)
                num_lines_test += 1
            line_count += 1
        print(f'Processed {line_count} lines.')
        print(f'Written {num_lines_train} lines in train.csv.')
        print(f'Written {num_lines_test} lines in test.csv.')
        print("Train and Test csv's generated")

def split_into_train_test(input_dir, output_dir):
    if os.path.isdir(output_dir):
        print("Train and Test folders already present. Skipping.......")
        return -1

    if not os.path.isdir(input_dir):
        print("Input directory--> {} is not valid.".format(input_dir))
        return -1

    else:
        print("Input directory is present")
        print("Creating output directory....")
        os.makedirs(output_dir)
        print("Creating one csv by aggregating all csv's...")

        csv_filenames = find_csv_filenames(input_dir)
        print("Creating one pandas dataframe for all the csv files...")
        df = pd.concat([pd.read_csv(csv_files) for csv_files in csv_filenames ])
        combined_csv = df.to_csv(os.path.join(output_dir,"walmart_labels.csv"),index=False)
        filenames = list(set(list(df['filename'].values)))
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

        # # Start reading the csv files to copy each row of associated filename to train and test accordingly
        generate_train_test_csv(train_filenames, test_filenames, train_test_dir=output_dir)
        #
        # generate_train_test_img_folders(input_dir, output_dir, train_filenames, test_filenames, resized, resize_factor)


