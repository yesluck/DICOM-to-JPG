import pydicom as dicom
import os
import cv2
import pandas as pd
import csv


def explore_folders(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.dcm'):
                yield os.path.join(root, file)


def convert_dcm_in_a_folder(folder_path, output_folder_path, png=True):
    # list of attributes available in dicom image
    # download this file from the given link # https://github.com/vivek8981/DICOM-to-JPG
    dicom_image_description = pd.read_csv("dicom_image_description.csv")

    with open(os.path.join(output_folder_path, f'Patient_Detail_{output_folder_path.split("/")[-1]}.csv'), 'w', newline ='') as csvfile:
        fieldnames = list(dicom_image_description["Description"])
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(fieldnames)
        for n, image in enumerate(explore_folders(folder_path)):
            ds = dicom.dcmread(image, force=True)
            rows = []
            try:
                pixel_array_numpy = ds.pixel_array
                image = image.split("/")[-1]
                if png == False:
                    image = image.replace('.dcm', '.jpg')
                else:
                    image = image.replace('.dcm', '.png')
                cv2.imwrite(os.path.join(output_folder_path, image), pixel_array_numpy)
                if n % 50 == 0:
                    print('{} image converted'.format(n))
                for field in fieldnames:
                    try:
                        if ds.data_element(field) is None:
                            rows.append('')
                    except:
                        pass
                        # print(field)
                    else:
                        x = str(ds.data_element(field)).replace("'", "")
                        y = x.find(":")
                        x = x[y+2:]
                        rows.append(x)
                writer.writerow(rows)
            except:
                print(image)


def process(input, output):
    if not os.path.exists(output):
        os.makedirs(output)

    for folder_name in os.listdir(input):
        input_path = os.path.join(input, folder_name)
        output_path = os.path.join(output, folder_name)
        if os.path.isdir(input_path):
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            convert_dcm_in_a_folder(input_path, output_path)


if __name__ == "__main__":
    process("input", "output")
