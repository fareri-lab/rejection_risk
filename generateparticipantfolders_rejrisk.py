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
import numpy as np



# read in raw qualtrics data and excel sheet of completed participants
# make csv into data frame
homedir = os.getcwd()
rawqualtrics = pd.read_csv('RejectionRisk_PhotoUpload_10222025.csv')
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
    subj_id = qualtrics['sub_ID'][i]
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
        sub_id = qualtrics['sub_ID'][sub]
        if len(os.listdir(indv_image_folder % (sub_id, sub_id))) == 30:
            continue
        else:
            if image.startswith(responseId): #the images still start with the qualtrics response id at this point, but we will change this to prolific id in the next section
                src = os.path.join(source_folder, image)
                dst = os.path.join(indv_image_folder %
                                   (sub_id, sub_id), image)
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
    sub_id = qualtrics['sub_ID'][sub]
    for p in os.listdir(participantimagefolder): #p = participant; for all ndividual folders in particpant image folder
        if not p.endswith('.DS_Store') or p.endswith('blank_file'): #we do not want DS store or blank file
            if p.startswith(sub_id): 
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
sociallevel = ["Rej", "Acc","Acc", "Rej"]
partnerlist = ['Charlie', 'Sam', 'Alex', 'Riley']
condition = ''
partner = ''
feedback = ''

for sub in range(0, len(qualtrics)):
    responseId = qualtrics['ResponseId'][sub]
    sub_id = qualtrics['sub_ID'][sub]
    for folder in os.listdir(participantimagefolder):
        if not folder.endswith('.DS_Store') or folder.endswith('blank_file'):
            if folder.startswith(sub_id):
                imagedir = indv_image_folder % (folder, folder) + '/'
                print(imagedir)
        
                os.chdir(imagedir)
                photolist = os.listdir(imagedir)
                pavlovia_path = imagedir.replace(
                    homedir + '/', "")
                photolist = [pavlovia_path + x for x in photolist]
        
                condition_selected = random.sample(sociallevel, 4)
                partner_selected = random.sample(partnerlist, 4)
                block = 0  # before experiment
                nTrials = 30
                alltrials = pd.DataFrame(columns=[
                                         'TrialNumber', 'Partner', 'Condition', 'Photos', 'Feedback', 'FeedbackWait'])
                alltrials['Partner'] = ''
                alltrials['Feedback'] = ''
                alltrials['Condition'] = ''
                alltrials['Photos'] = ''
                # for k in range(0,len(photolist)):
                for i in range(0, 4):
                    if condition_selected[i] == 'Rej':
                        pDislike = .8
                        pLike = .2
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
        
                  
                subid = folder
                expdir = participantimagefolder
                
                input_file = os.path.join(homedir, 'choiceset_30.xlsx')

                # Load raw Excel contents
                # Load the full sheet including header (row 0)
                full_df = pd.read_excel(input_file)
                
                # Extract the header (row 0 is automatically header, so full_df.columns are headers)
                # Extract rows 1 to 31 (pandas uses 0-based indexing, so rows 1:32 to include row 31)
                data_rows = full_df.iloc[0:30].copy()  # 31 rows to shuffle
                
                columns_to_keep = ['ev_level', 'risky_gain', 'certain']
                data_subset = data_rows[columns_to_keep]
                
                # Shuffle into 4 independent blocks (no outcomes yet)
                shuffled_blocks = pd.concat(
                    [data_subset.sample(frac=1).reset_index(drop=True) for _ in range(4)],
                    ignore_index=True
                )
                
                # Create outcome list: 60 wins, 60 losses
                outcomes = ['w'] * 60 + ['l'] * 60
                np.random.shuffle(outcomes)
                
                # Assign to outcome column
                shuffled_blocks['outcome'] = outcomes
                
                # Convert to float and round to 2 decimal places
                shuffled_blocks['certain'] = shuffled_blocks['certain'].astype(float).round(2)
                shuffled_blocks['risky_gain'] = shuffled_blocks['risky_gain'].astype(float).round(2)
                                
                # Save
                gambles_sheet = '%s/%s_gambles.csv' % (subj_dir, subid)
                shuffled_blocks.to_csv(gambles_sheet, index=False)
                

                
                print(f"Saved gambles file to: {gambles_sheet}")


                                
                                
                alltrials['FeedbackWait'] = spreadsheet['FeedbackWait']
                subjdir = '%s/%s' % (expdir, subid)
                trial_sheet = '%s/%s_trials.csv' % (subjdir, subid)
                alltrials['TrialNumber'] = range(1, len(alltrials)+1)
                alltrials.to_csv(trial_sheet, index=False)

                gambles_sheet = '%s/%s_gambles.csv' % (subjdir, subid)
                alltrials.to_csv(trial_sheet, index=False)
