import os
import pickle
import csv
from collections import namedtuple
import re
from multidict import MultiDict
from math import *

MIN_NUM_IMAGES = 50
MAX_NUM_IMAGES = 200
NUM_CHOSEN_PARTICIPANTS = 1500

ImageDesc = namedtuple('ImageDesc', ['site', 'alt_site_name', 'participant', 'event', 'img_index', 'zip_file', 'path_in_zip'])

zip_list_name = r'C:\Users\leahb\Documents\Leah\MyDataSets\ListOfZipsNoTaino+OSS.csv'
cClean_no_meir_list_name = r'C:\Users\leahb\Documents\Leah\MyDataSets\FileSelection\old\cCleanListNoTainoNoMeir.csv'
zip_and_cClean_no_meir_list = r'C:\Users\leahb\Documents\Leah\MyDataSets\FileSelection\old\ZipCCleanNoMeir.csv'

extension_regex = re.compile('\\.(zip|rar)/')

sites_with_particicipants_names =  ["Knickerbocker_Village", "NewYork_Housing", "Babcock"]

def extract_site_name_and_participant (site_participant):

    separator = site_participant.rfind('_')
    participant_name = site_participant[separator + 1:]

    for site_name in sites_with_particicipants_names:
        if site_participant.startswith(site_name):
            return(site_name, participant_name)

    site_name = site_participant[:separator]

    return (site_name, participant_name)

def main ():
    with open(cClean_no_meir_list_name, 'r', errors='replace') as cClean_no_meir_list_file:
        csvfile = csv.reader(cClean_no_meir_list_file)
        cClean_no_meir_list = []
        site_names = set()
        site_names_and_participants = set()
        for row in csvfile:
            if len(row) == 0:
                continue
            cClean_no_meir_list.append(row[0])
            site_participant,  = row
            site_name, partipant_name = extract_site_name_and_participant (site_participant)
            site_names.add (site_name)
            site_names_and_participants.add ((site_name, partipant_name))

    cclean_site_names_list = list(site_names)
    cclean_site_names_list.sort()
    image_descriptions = []
    #print ("cClean site names: \n", '\n'.join(cclean_site_names_list))

    with open(zip_list_name, 'r', errors='replace') as zip_list:
        csvfile = csv.reader(zip_list)
        site_names = dict()

        with open(zip_and_cClean_no_meir_list, 'wt') as zip_ccclean_noMeir_file:
            csvwriter = csv.writer (zip_ccclean_noMeir_file)
            csvwriter.writerow(ImageDesc._fields)

            for row in csvfile:
                site_participant, filename = row

                separator = site_participant.rfind('_')
                site = site_participant[:separator]

                filename = filename.replace('\\', '/')
                filename_base = filename[:-4] # cut off '.jpg'
                parts = filename_base.split('/')
                alt_site_name, participant, event, img_index = parts[-4:]

                if site == "SingTel":
                    alt_site_name = "SingTel"

                if site == "KippsBay":
                    alt_site_name = "KBCBMSVR1"

                if site == "SeaView":
                    alt_site_name = "SVS1-HZ-ISR"

                match = extension_regex.search(filename)
                if match is None:
                    raise Exception('Not an archive')

                zip_file = filename[:match.end() - 1]
                path_in_zip = filename[match.end():]

                desc = ImageDesc(site, alt_site_name, participant, event, img_index, zip_file, path_in_zip)
                site_names[site] = alt_site_name
                site_names[alt_site_name] = site

                if (site,participant) in site_names_and_participants or (alt_site_name, participant) in site_names_and_participants:
                    image_descriptions.append(desc)
                    csvwriter.writerow (desc)

    participant_to_images = MultiDict()

    for desc in image_descriptions:
        participant_to_images.add(str((desc.site, desc.participant)), desc)

    chosen_site_to_participant = MultiDict()
    selected_image_descriptions = []
    for participant in set(participant_to_images.keys()):
        images = participant_to_images.getall(participant)
        if len(images) > MIN_NUM_IMAGES and len(images) <= MAX_NUM_IMAGES:
            # selected_image_descriptions += images
            chosen_site_to_participant.add(images[0].site, images[0].participant)

    num_chosen_participants_per_site = dict()
    for site in set(chosen_site_to_participant.keys()):
        num_chosen_participants_per_site[site] = len(chosen_site_to_participant.getall(site))
        print(site, num_chosen_participants_per_site[site])

    total_num_chosen_participants = sum(num_chosen_participants_per_site.values())
    print(total_num_chosen_participants, 'total')

    for site, num_part in num_chosen_participants_per_site.items():
        ratio = num_part / total_num_chosen_participants
        num_participants_to_select = round(ratio * NUM_CHOSEN_PARTICIPANTS)
        print(site, num_part, ratio, num_participants_to_select)

        if num_participants_to_select == 0:
            continue

        participants = chosen_site_to_participant.getall(site)
        participants = participants[:num_participants_to_select]

        for participant in participants:
            images = participant_to_images.getall(str((site, participant)))

            per_event = MultiDict()
            for img in images:
                per_event.add(img.event, img)

            num_events = len(set(per_event.keys()))
            images_per_event = ceil(MIN_NUM_IMAGES / num_events)
            selected_images_for_this_participant = []
            for event in set(per_event.keys()):
                images_for_this_event = per_event.getall(event)
                selected_images_for_this_participant += images_for_this_event[:images_per_event]

            if len(selected_images_for_this_participant) >= MIN_NUM_IMAGES:
                selected_images_for_this_participant = selected_images_for_this_participant[:MIN_NUM_IMAGES]
            else:
                selected_images_set = set(selected_images_for_this_participant)
                for img in images:
                    selected_images_set.add(img)
                    if len(selected_images_set) == MIN_NUM_IMAGES:
                        break
                selected_images_for_this_participant = list(selected_images_set)

            selected_image_descriptions += selected_images_for_this_participant

    outfile = open(r'C:\Users\leahb\Documents\Leah\MyDataSets\FileSelection\selected_images_for_unknown.csv', 'wt', encoding='ascii')
    csv_out = csv.writer(outfile)
    csv_out.writerow(ImageDesc._fields)
    for rec in selected_image_descriptions:
        csv_out.writerow(rec)

main()