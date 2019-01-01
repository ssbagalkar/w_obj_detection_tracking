# This file will handle the pre-processing of the data
import os
from bulk_rename import rename_files
from bulk_resize import resize_files_and_annotations
from convert_xml_to_csv import xml_to_csv
from train_test_split_data import split_into_train_test

def preprocess_data(image_dir, split_data=False, resize=False, rename = False):

    # optionally rename the data
    if rename:
        rename_files(image_dir)

    # Convert xmls to csv
    for image_path in os.listdir(image_dir):
        if os.path.isdir(os.path.join(image_dir,image_path)):
            done = xml_to_csv(os.path.join(image_dir,image_path))
            if done:
                print('Successfully converted xml to csv for {}.'.format(image_path))

    if split_data:
        output_dir = os.path.join(os.path.dirname(image_dir), "train_test")
        split_into_train_test(image_dir, output_dir)

    # optionally resize the data
    if resize:
        output_dir = os.path.join(os.path.dirname(image_dir), "train_test")
        for image_path in os.listdir(output_dir):
            if os.path.isdir(os.path.join(os.path.dirname(image_dir),'train_test',image_path)):
                if image_path == 'test':
                    csv_file_name = 'test_labels.csv'
                else:
                    csv_file_name = 'train_labels.csv'
                resize_files_and_annotations(image_dir=os.path.join(output_dir,image_path), out_dir=os.path.join(output_dir,image_path), csv_file = csv_file_name, scale_factor_x=8,
                                         scale_factor_y=8, resize_in_place=True)

image_dir = "E:\\raw_data\\data"
preprocess_data(image_dir, split_data=False, resize=True, rename=False)