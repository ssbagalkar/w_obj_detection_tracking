import os
import pandas as pd
import xml.etree.ElementTree as ET
import json
import glob
print("All import successful")


def xml_to_csv(path):
    xml_list=[]
    num_files_converted = 0
    if not os.path.isfile(os.path.join(path,path.split("\\")[-1]+"walmart_labels.csv")):
        for xml_file in glob.glob(path + '/*/*.xml'):
            print("Processing xml to csv for --> {}".format(xml_file.split("\\")[-1]))
            tree = ET.parse(xml_file)
            root = tree.getroot()
            print("Current image --> {}".format(root.find('filename').text))
            num_objects = 1
            for member in root.findall('object'):
                print("--------- Object --> {} --------".format(num_objects))
                name_idx=0
                bndbox_idx = 0
                for attrib in member:
                    if attrib.tag == 'name':
                        name_subchild = json.loads(member[name_idx].text)
                        break
                    name_idx+=1
                for attrib in member:
                    if attrib.tag == 'bndbox':
                        break
                    bndbox_idx+=1
                for key,value in name_subchild.items():
                    if key == 'class':
                        if value != 'hand' and value != 'item':
                            print("Appending for class {}".format(value))
                            val = value
                            value = (xml_file.split("\\")[-1].split(".")[0],
                                     int(root.find('size')[0].text),
                                     int(root.find('size')[1].text),
                                     val,
                                     int(member[bndbox_idx][0].text),
                                     int(member[bndbox_idx][1].text),
                                     int(member[bndbox_idx][2].text),
                                     int(member[bndbox_idx][3].text)
                                     )
                            print("Appending {}".format(value))
                            xml_list.append(value)

                        else:
                            print("Not entering!!")
                num_objects+=1
            num_files_converted+=1
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        image_dir = path.rsplit("\\", 1)[-1]
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        xml_df.to_csv(path + "\\" + image_dir + 'walmart_labels.csv', index=None)
    else:
        print("{} already has a csv file".format(path.rsplit("\\")[-1]))
    print("Number of processed files -- > {}".format(num_files_converted))

    if num_files_converted!=0:
        print("XML to CSV converted")
        return True
    else:
        print("XML to CSV not converted as CSV already present")
        return False
