import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import json
import csv
import glob
print("All import successful")

def xml_to_csv(path):
	xml_list=[]
	num_files_converted = 0
	for xml_file in glob.glob(path + '/*.xml'):
		tree = ET.parse(xml_file)
		root = tree.getroot()
		print("Current image --> {}".format(root.find('filename').text))
		num_objects = 1
		for member in root.findall('object'):
			print("--------- Object --> {} --------".format(num_objects))
			name_subchild = json.loads(member[4].text)
			print(name_subchild)
			for key,value in name_subchild.items():
				if key == 'class':
					if value != 'hand' and value != 'item':
						print("Appending for class {}".format(value))
						val = value
						value = (root.find('filename').text,
						int(root.find('size')[0].text),
						int(root.find('size')[1].text),
						val,
						int(member[3][0].text),
						int(member[3][1].text),
						int(member[3][2].text),
						int(member[3][3].text)
						)
						print("Appending {}".format(value))
						xml_list.append(value)
					
					else:
						print("Not entering!!")
			num_objects+=1
		num_files_converted+=1
	print("Number of processed files -- > {}".format(num_files_converted))
	column_name = ['filename', 'width','height','class','xmin','ymin','xmax','ymax']	
	xml_df = pd.DataFrame(xml_list, columns=column_name)
	return xml_df

def main():
	image_path = os.path.join(os.getcwd(), '../walmart_data/annotations')
	xml_df = xml_to_csv(image_path)
	xml_df.to_csv('walmart_labels.csv', index=None)
	print('Successfully converted xml to csv.')


main()
