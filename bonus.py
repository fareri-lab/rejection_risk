#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 08:31:42 2025

@author: jordansiegel
"""

import os
import pandas as pd
import random

#user input to gather subject id and which version of task used for sub
subj_id= input('(Experimenter only) Please enter participant ID:')

#get current working directory
expdir = os.getcwd()

#get current subject directory
data_folder = '%s/data' % (expdir)
data_file = pd.read_csv('%s/%s_RejTask_2025-07-24_12h24.50.csv' %(data_folder,subj_id))

#randomly select trial
bonus_trial = random.randint(1,120)

# get the row for that trial
row = data_file.loc[data_file['GambleTrialNumber'] == bonus_trial]

if not row.empty:
    choice_code = int(row['GambleChoice'].iloc[0])
    selected_price = row['SelectedPrice'].iloc[0]  # <-- pulls price for same trials

    if choice_code == 0:
        choice_text = "Certain"
    elif choice_code == 1:
        choice_text = "Gamble"
    elif choice_code == 9:
        choice_text = "Missed trial"
    else:
        choice_text = "Unknown code"

    #print(f"Bonus trial: {bonus_trial}")
    #print(f"Choice code: {choice_code} → {choice_text}")
else:
    print(f"No row found for trial {bonus_trial}")
    

#print summary
print('Participant: %s' %(subj_id))
print('Trial: %s' %(bonus_trial))
print('Choice: %s' %(choice_text))
print('Bonus: $%s' %(selected_price))
print('-----------------------')