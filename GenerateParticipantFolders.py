#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 12:27:50 2022

@author: Melanie Ruiz and Jordan Siegel
"""

import os
import pandas as pd
import random
import shutil


# read in raw qualtrics data and excel sheet of completed participants
# make csv into data frame
homedir = os.getcwd()
rawqualtrics = pd.read_csv('RejectionChoice_PhotoUpload_882023.csv')
completedparticipantlist = pd.read_excel('participantlist.xlsx')
completedparticipantlist = completedparticipantlist.loc[
    completedparticipantlist['PhotosUploaded? (y/n)'] == 'n']

# %%
# remove uneeded rows from data frame from raw qualtrics data
rawqualtrics = rawqualtrics.drop([0, 1])

# reset index numbers for raw qualtrics dats
rawqualtrics = rawqualtrics.reset_index()

# gathering sub_ids of completed participants only
qualtrics = rawqualtrics.loc[rawqualtrics['ResponseId'].isin(
    completedparticipantlist['photouploadsub_id'])]
qualtrics = qualtrics.reset_index()

# %%
#creates blank foldrs for each participant
# setcurrentworking directory to a variable
#create participant folders using their PROLIFIC ID, instead of the qualtrics id
expdir = os.getcwd()

image_dir = ''
# make new folders for each participant and then a folder in each new folder
for i in range(0, len(qualtrics)):
    subj_id = qualtrics['PROLIFIC_PID'][i]
    subj_dir = '%s/Participant_Images/%s' % (expdir, subj_id)
    if os.path.exists(subj_dir):
        continue
    else:
        os.makedirs(subj_dir)
        image_dir = '%s/%s_Images' % (subj_dir, subj_id)
        os.makedirs(image_dir)

    # if not os.path.exists (subj_dir):
    #     os.makedirs(subj_dir)
    # else:
    #     continue

    # image_dir = '%s/%s_Images' % (subj_dir,subj_id)
    # if not os.path.exists (image_dir):
    #     os.makedirs(image_dir)
    # else:
    #     continue
# %%
#move all raw individual participant images from Raw_Participant_Images to their own respective participant folders
source_folder = expdir + '/Raw_Participant_Images/'
qual_photo_folders = [f.path for f in os.scandir(source_folder) if f.is_dir()]
indv_image_folder = expdir + '/Participant_Images/%s/%s_Images'

# the directory tree is as follows: Raw_Participant_Images/Photo_1/photo, etc
# move every individual photo out of the photo_n folders
# Photo_Folder = every photo_n folder
# f= an individual photo in a given photo_n folder

for Photo_Folder in qual_photo_folders:
    for f in os.listdir(Photo_Folder):
        src = os.path.join(Photo_Folder, f)
        dst = os.path.join(source_folder, f)
        shutil.move(src, dst)
# delete all empty photo_n folders
for Photo_Folder in qual_photo_folders:
    shutil.rmtree(Photo_Folder)
# image = every individual extracted image now freely existing in Raw_Participant_Images
for image in os.listdir(source_folder):
    # for every subject listed in the qualtrics dataframe
    for sub in range(0, len(qualtrics)):
        responseId = qualtrics['ResponseId'][sub]
        prolificId = qualtrics['PROLIFIC_PID'][sub]
        if len(os.listdir(indv_image_folder % (prolificId, prolificId))) == 30:
            continue
        else:
            if image.startswith(responseId): #the images still start with the qualtrics response id at this point, but we will change this to prolific id in the next section
                src = os.path.join(source_folder, image)
                dst = os.path.join(indv_image_folder %
                                   (prolificId, prolificId), image)
                shutil.move(src, dst)


# creates variables to take files out of folders,move them to a different folder, and delete the original folders

# exceuting moving files from subfolders to a different folder and then deleting the old subfolders

# %%

#RENAME the images so that they start with the PROLIFIC ID, instead of the qualtrics response ID 
# count increase by 1 in each iteration
# iterate all files from a directory
participantimagefolder = expdir + '/Participant_Images/' #parent folder for all participant folders and their renamed images
count = 1
for sub in range(0, len(qualtrics)):
    responseId = qualtrics['ResponseId'][sub]
    prolificId = qualtrics['PROLIFIC_PID'][sub]
    for p in os.listdir(participantimagefolder): #p = participant; for all ndividual folders in particpant image folder
        if not p.endswith('.DS_Store') or p.endswith('blank_file'): #we do not want DS store or blank file
            if p.startswith(prolificId): 
                count = 1
                for photo in os.listdir(indv_image_folder % (p, p)):
                    if "_Image_" in photo:
                        continue
                    else:
                        if photo.endswith('.jpg') or photo.endswith('.jpeg') or photo.endswith('.png') or photo.endswith('.JPG') or photo.endswith('.JPEG') or photo.endswith('.PNG'):
                            # Construct old file name
                            source = indv_image_folder % (p, p) + '/' + photo
                            # Adding the count to the new file name and extension
                            file_name, file_extension = os.path.splitext(photo)
    
                            destination = indv_image_folder % (
                                p, p) + '/' + p + "_Image_" + str(count) + ".jpeg"
                            # Renaming the file
                            os.rename(source, destination)
                            count += 1


# %%

# insert  code to skip if a csv file already exists
# change qualtrics ID to PROLIFIC ID
spreadsheet = pd.read_csv('spreadsheet_template.csv')
sociallevel = ["Rej", "Acc", "Neutral", "Acc", "Rej"]
partnerlist = ['Charlie', 'Sam', 'Riley', 'Alex', 'Taylor']
condition = ''
partner = ''
feedback = ''

for sub in range(0, len(qualtrics)):
    responseId = qualtrics['ResponseId'][sub]
    prolificId = qualtrics['PROLIFIC_PID'][sub]
    for folder in os.listdir(participantimagefolder):
        if not folder.endswith('.DS_Store') or folder.endswith('blank_file'):
            if folder.startswith(prolificId):
                imagedir = indv_image_folder % (folder, folder) + '/'
                print(imagedir)
        
                os.chdir(imagedir)
                photolist = os.listdir(imagedir)
                pavlovia_path = imagedir.replace(
                    homedir + '/', "")
                photolist = [pavlovia_path + x for x in photolist]
        
                condition_selected = random.sample(sociallevel, 5)
                partner_selected = random.sample(partnerlist, 5)
                block = 0  # before experiment
                nTrials = 30
                alltrials = pd.DataFrame(columns=[
                                         'TrialNumber', 'Partner', 'Condition', 'Photos', 'Feedback', 'FeedbackWait'])
                alltrials['Partner'] = ''
                alltrials['Feedback'] = ''
                alltrials['Condition'] = ''
                alltrials['Photos'] = ''
                # for k in range(0,len(photolist)):
                for i in range(0, 5):
                    if condition_selected[i] == 'Rej':
                        pDislike = .7
                        pLike = .3
                        rej = pd.DataFrame(
                            columns=['Partner', 'Condition', 'Photos', 'Feedback'])
                        partner = partner_selected[i]
                        condition = condition_selected[i]
                        blocklist = ['did not like'] * \
                            int(nTrials * pDislike) + ['liked'] * int(nTrials * pLike)
                        random.shuffle(blocklist)
                        feedback = random.sample(blocklist, 30)
                        photo_selected = random.sample(photolist, 30)
                        rej['Feedback'] = feedback
                        rej['Partner'] = partner
                        rej['Condition'] = condition
                        rej['Photos'] = photo_selected
                        alltrials = pd.concat([alltrials, rej], ignore_index=True)
        
                    elif condition_selected[i] == 'Acc':
                        pDislike = .3
                        pLike = .7
                        acc = pd.DataFrame(
                            columns=['Partner', 'Condition', 'Photos', 'Feedback'])
                        partner = partner_selected[i]
                        condition = condition_selected[i]
                        blocklist = ['did not like'] * \
                            int(nTrials * pDislike) + ['liked'] * int(nTrials * pLike)
                        random.shuffle(blocklist)
                        feedback = random.sample(blocklist, 30)
                        photo_selected = random.sample(photolist, 30)
                        acc['Feedback'] = feedback
                        acc['Partner'] = partner
                        acc['Condition'] = condition
                        acc['Photos'] = photo_selected
                        alltrials = pd.concat([alltrials, acc], ignore_index=True)
        
                    elif condition_selected[i] == 'Neutral':
                        pDislike = .5
                        pLike = .5
                        neu = pd.DataFrame(
                            columns=['Partner', 'Condition', 'Photos', 'Feedback'])
                        partner = partner_selected[i]
                        condition = condition_selected[i]
                        blocklist = ['did not like'] * \
                            int(nTrials * pDislike) + ['liked'] * int(nTrials * pLike)
                        random.shuffle(blocklist)
                        feedback = random.sample(blocklist, 30)
                        photo_selected = random.sample(photolist, 30)
                        neu['Feedback'] = feedback
                        neu['Partner'] = partner
                        neu['Condition'] = condition
                        neu['Photos'] = photo_selected
                        alltrials = pd.concat([alltrials, neu], ignore_index=True)
                subid = folder
                expdir = participantimagefolder
                alltrials['FeedbackWait'] = spreadsheet['FeedbackWait']
                subjdir = '%s/%s' % (expdir, subid)
                trial_sheet = '%s/%s_trials.csv' % (subjdir, subid)
                alltrials['TrialNumber'] = range(1, len(alltrials)+1)
                alltrials.to_csv(trial_sheet, index=False)
#%%
#Delete all extraneous photos in Raw_Participant_Folder (sourcefolder)
# for f in os.listdir(source_folder):
#     os.remove(os.path.join(source_folder, f))
# os.chdir(source_folder)
# with open("blank_file", "w") as f:
#         f.write("2")
