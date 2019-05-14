import os
from os.path import join
from zipfile import ZipFile
from rarfile import RarFile
import shutil
import csv

zip_dir = r'H:\Data_Management\From_Zips'
out_file_name = r'C:\Users\leahb\Documents\Leah\zip_directory.csv'

out_file = open(out_file_name, 'wt', newline='')
out_file_csv = csv.writer(out_file)

subdirs = os.listdir(zip_dir)
for subdir in subdirs:
    if not os.path.isdir(join(zip_dir, subdir)):
        continue

    clean_data_dir = join(zip_dir, subdir, r'Clean_data')
    if not os.path.isdir(clean_data_dir):
        print(clean_data_dir, ' is not a directory')
        continue

    files = os.listdir(clean_data_dir)
    zipfiles = [f for f in files if f.endswith('.zip') or f.endswith('.rar')]
    if len(zipfiles) == 0:
        print('No zip files in ', clean_data_dir)
        continue

    for zipfile_name in zipfiles:
        full_path = join(clean_data_dir, zipfile_name)
        print(full_path)
        zip = ZipFile(full_path, 'r') if zipfile_name.endswith('.zip') else RarFile(full_path, 'r')
        for filename in zip.namelist():
            if filename.endswith('.jpg'):
                out_file_csv.writerow((full_path, filename))