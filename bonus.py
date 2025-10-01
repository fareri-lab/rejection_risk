#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 08:31:42 2025

@author: jordansiegel
"""

import os
import pandas as pd
import random
import glob 

#user input to gather subject id and which version of task used for sub
subj_id= input('(Experimenter only) Please enter participant ID:')

#get current working directory
expdir = os.getcwd()

# get current subject directory
data_folder = os.path.join(expdir, "data")

# build file pattern: subjID_RejTask_*.csv
pattern = os.path.join(data_folder, f"{subj_id}_RejTask_*.csv")

# find all matching files
file_list = glob.glob(pattern)

if len(file_list) == 1:
    # only one match, read it
    data_file = pd.read_csv(file_list[0])
    print(f"Loaded file: {file_list[0]}")
else:
    # multiple matches, print them
    print("Multiple matching files found:")
    for f in file_list:
        print(f)
    print("Please select which file to use or rename duplicates.")
    
#randomly select trial
bonus_trial = random.randint(1,120)

# get the row for that trial
row = data_file.loc[data_file['GambleTrialNumber'] == bonus_trial]

if not row.empty:
    choice_code = int(row['GambleChoice'].iloc[0])
    selected_price = row['SelectedPrice'].iloc[0]  # pulls price for same trial
    outcome = row['Outcome'].iloc[0]  # assuming your column is named 'Outcome'

    if choice_code == 0:
        choice_text = "Certain"
        bonus_amount = selected_price  # they get the selected price for certain choice
    elif choice_code == 1:
        choice_text = "Gamble"
        # assign bonus based on outcome
        if outcome.lower() == 'w':
            bonus_amount = selected_price
        elif outcome.lower() == 'l':
            bonus_amount = 0
        else:
            bonus_amount = None  # or handle unexpected outcome codes
    elif choice_code == 999:
        choice_text = "Missed trial"
        bonus_amount = "Missed Trial"
    else:
        choice_text = "Unknown code"
        bonus_amount = 0

else:
    print(f"No row found for trial {bonus_trial}")
    choice_text = "No trial"
    bonus_amount = 0

#print summary
print('Participant: %s' % (subj_id))
print('Trial: %s' % (bonus_trial))
print('Choice: %s' % (choice_text))
print('Bonus: $%s' % (bonus_amount))
print('-----------------------')