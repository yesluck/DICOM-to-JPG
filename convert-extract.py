import pydicom as dicom
import matplotlib.pyplot as plt
import os
import cv2
import PIL # optional
import pandas as pd
import csv
# make it True if you want in PNG format
PNG = True
# Specify the .dcm folder path
folder_path = "zhang_guodong____AND_49_MORE"
# Specify the .jpg/.png folder path
jpg_folder_path = "PNG_test"
images_path = os.listdir(folder_path)
# list of attributes available in dicom image
# download this file from the given link # https://github.com/vivek8981/DICOM-to-JPG
dicom_image_description = pd.read_csv("dicom_image_description.csv")

with open('Patient_Detail.csv', 'w', newline ='') as csvfile:
    fieldnames = list(dicom_image_description["Description"])
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldnames)
    for n, image in enumerate(images_path):
        ds = dicom.dcmread(os.path.join(folder_path, image))
        rows = []
        try:
            pixel_array_numpy = ds.pixel_array
            if PNG == False:
                image = image.replace('.dcm', '.jpg')
            else:
                image = image.replace('.dcm', '.png')
            cv2.imwrite(os.path.join(jpg_folder_path, image), pixel_array_numpy)
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