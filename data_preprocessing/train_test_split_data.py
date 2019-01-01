
import os
import pandas as pd
import numpy as np
import csv
import shutil


def find_csv_filenames( path_to_dir, suffix=".csv" ):
    all_cases = os.listdir(path_to_dir)
    all_case_locations = [os.path.join(path_to_dir,case) for case in all_cases ]
    csv_files=[]
    for case in all_case_locations:
        for filename in os.listdir(case):
            if filename.endswith(suffix):
                csv_files.append(os.path.join(path_to_dir,case,filename))
    return csv_files


def generate_train_test_csv(train_filenames, test_filenames, train_test_dir ):

    # declare all paths
    original_csv_path = os.path.join(train_test_dir, 'walmart_labels.csv')
    print("Creating train folder...")
    if not os.path.isdir(os.path.join(train_test_dir, 'train', 'data')):
        os.makedirs(os.path.join(train_test_dir,'train', 'data'))
    if not os.path.isdir(os.path.join(train_test_dir, 'train', 'labels')):
        os.makedirs(os.path.join(train_test_dir, 'train', 'labels'))
    print("Creating test folder...")
    if not os.path.isdir(os.path.join(train_test_dir, 'test', 'data')):
        os.makedirs(os.path.join(train_test_dir, 'test', 'data'))
    if not os.path.isdir(os.path.join(train_test_dir, 'test', 'labels')):
        os.makedirs(os.path.join(train_test_dir, 'test', 'labels'))
    train_csv_path = os.path.join(train_test_dir,'train','labels', 'train_labels.csv')
    test_csv_path = os.path.join(train_test_dir, 'test', 'labels', 'test_labels.csv')


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

def generate_train_test_data(train_filenames, test_filenames, train_test_dir, input_dir ):
    print("\t\t")
    print("Copying all images in training set...")
    print("Training set has {} images...".format(len(train_filenames)))
    for train_file in train_filenames:
        train_img = train_file.split(".xml")[0]+".png"
        case = train_img.split("_frame")[0]
        if os.path.isfile(os.path.join(train_test_dir,'train','data',train_img)):
            print("Train directory already has {}. Skipping...".format(train_file))
            continue
        print("Copying {} to train folder".format(train_img))
        shutil.copy2(os.path.join(input_dir,case,'frames',train_img),os.path.join(train_test_dir,'train','data'))
    print("All train images copied")
    print("\t")

    print("Copying all images in test set...")
    for test_file in test_filenames:
        test_img = test_file.split(".")[0]+".png"
        case = test_img.split("_frame")[0]
        if os.path.isfile(os.path.join(train_test_dir,'test','data',test_img)):
            print("Test directory already has {}. Skipping...".format(test_file))
            continue
        print("Copying {} to test folder...".format(test_img))
        shutil.copy2(os.path.join(input_dir,case,'frames',test_img),os.path.join(train_test_dir,'test','data'))
    print("All test images copied.")





def split_into_train_test(input_dir, output_dir):
    # if os.path.isdir(output_dir):
    #     print("Train and Test folders already present. Skipping.......")
    #     return -1

    if not os.path.isdir(input_dir):
        print("Input directory--> {} is not valid.".format(input_dir))
        return -1

    else:
        print("Input directory is present")
        if not os.path.isdir(output_dir):
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

        generate_train_test_csv(train_filenames, test_filenames, train_test_dir=output_dir)
        generate_train_test_data(train_filenames, test_filenames, train_test_dir=output_dir, input_dir=input_dir)



