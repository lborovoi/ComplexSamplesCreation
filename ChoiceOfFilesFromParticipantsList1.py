import os
import pickle
import random
import csv

NUM_IMAGES = 50
NUM_CHOSEN_PARTICIPANTS = 5000

base_dir = r'W:\train_data\cClean\\'

with open (r'C:\Users\leahb\Documents\Leah\MyDataSets\FileSelection\PotencialForUnknown.csv', "rt") as list_of_participants:
    list_of_participants_names = list_of_participants.readlines()

with open(r'C:\Users\leahb\Documents\Leah\MyDataSets\tmp\directory_contents1.pickle', "rb") as pickle_file:
  list_of_images = pickle.load(pickle_file)

counter = 0

with open (r'C:\Users\leahb\Documents\Leah\MyDataSets\FileSelection\unknown_images2.csv', "wt") as images_file:
    csvfile = csv.writer(images_file)
    for row in list_of_participants_names:
        id = row.strip()
        if counter > NUM_CHOSEN_PARTICIPANTS:
            print((id,image))
            break

        images = list_of_images[id]
        if len(images) < NUM_IMAGES:
                print(id)
                continue
        random.shuffle(images)
        images = images[:NUM_IMAGES]
        counter += 1
        for image in images:
            csvfile.writerow((id,image))
            #print((id,image))



    #print (meir_file_names)
#meir_file_names = set(meir_file_names)
#cCleanList_names = set (cCleanList)

#with open (r'C:\Users\leahb\Documents\Leah\inessa\FileNamesDataWithoutMeir.csv', "rt") as all_data_file:
 #  all_data_file_names = all_data_file.readlines()
 #  all_data_file_names = set(all_data_file_names)

#not_trained_list = all_data_file_names - meir_file_names
#print (not_trained_list)

