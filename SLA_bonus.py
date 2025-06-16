import os
import pandas as pd
import random

#user input to gather subject id and which version of task used for sub
subj_id= input('(Experimenter only) Please enter participant ID:')

version = input('version: ')

#randomly select self run
self_run = random.randint(1,3)


#initilaize friend variable
friend_run = ''

#get current working directory
expdir = os.getcwd()

#get current subject directory
subjdir = '%s/logs/%s' % (expdir, subj_id)

#determine which version to pull "friend" files from
if str(version) == '1':
    friend_run = random.randint(4,6)
elif str(version) == '2':
    friend_run = random.randint(7,9)

#set up condition count for cases where there are return sessions (i.e. more than one file ending with the same run number)
selfrun_count = sum(1 for i in os.listdir(subjdir) if i.endswith('%s.csv' %(self_run)))
friendrun_count = sum(1 for i in os.listdir(subjdir) if i.endswith('%s.csv' %(friend_run)))
print("Number of times self is in list:\n",selfrun_count)
print("Number of times friend is in list:\n",friendrun_count)


#read in randomly selected self run
for file in os.listdir(subjdir):
    if selfrun_count > 1:
        self_file = pd.read_csv('%s/sub-%s_SLAempathy_REDO_run-0%s.csv' %(subjdir,subj_id, self_run))

    else:
        if file.endswith('%s.csv' %(self_run)):
            print(file)
            self_file = pd.read_csv('%s/%s' %(subjdir, file))

#read in randomly selected friend run
for file in os.listdir(subjdir):
    if friendrun_count > 1:
        friend_file = pd.read_csv('%s/sub-%s_SLAempathy_REDO_run-0%s.csv' %(subjdir,subj_id, friend_run))
    else:
        if file.endswith('%s.csv' %(friend_run)):
            print(file) 
            friend_file = pd.read_csv('%s/%s' %(subjdir, file))

#randomly select trial for both self and friend

self_trial = random.randint(1,32)
friend_trial = random.randint(1,32)


#store choice
self_choice = self_file['bpress'][self_trial-1]
friend_choice = friend_file['bpress'][friend_trial-1]


if self_choice == 6:
    self_choicetext = 'Lottery'
    self_outcome = 'Outcome: %s' %(self_file['task_gamble_outcome'][self_trial-1])
elif self_choice == 1:
    self_choicetext = 'Guaranteed'
    self_outcome = 'Outcome: %s' %(self_file['alt_certain'][self_trial-1])

elif self_choice == 999:
    self_choicetext = 'No response detected'
    self_outcome = '$0'
    

if friend_choice == 6:
    friend_choicetext = 'Lottery'
    friend_outcome = 'Outcome: %s' %(friend_file['task_gamble_outcome'][friend_trial-1])
elif friend_choice == 1:
    friend_choicetext = 'Guaranteed'
    friend_outcome = 'Outcome: %s' %(friend_file['alt_certain'][friend_trial-1])

elif friend_choice == 999:
    friend_choicetext = 'No response detected'

#if lottery

# message to display if the trial was skipped
skip_msg = '$0 - Missed trial'


#%%
# get exact earnings from trial sheet
self_bonus = self_file['trial_earning'][self_trial-1]
friend_bonus = friend_file['trial_earning'][friend_trial-1]

#if trial is missed, bonus = 0

    
if self_bonus == -24 or self_bonus == 0:
    print('missed trial: %s' %(self_bonus))
    self_bonus = '$0 - Total loss from lottery :('
if friend_bonus == -24 or self_bonus == 0:
    print('missed trial: %s' %(friend_bonus))
    friend_bonus = '$0 - Total loss from lottery :('

#print summary
print('Participant')
print('Run: %s' %(self_run))
print('Trial: %s' %(self_trial))
print('Choice: %s' %(self_choicetext))
print('Outcome: %s' %(self_file['choice_amount'][self_trial-1]))
print('Bonus: $%s' %(self_bonus))
print('-----------------------')

print('Friend')
print('Run: %s' %(friend_run))
print('Trial: %s' %(friend_trial))
print('Choice: %s' %(friend_choicetext))
print('Outcome: %s' %(friend_file['choice_amount'][friend_trial-1]))
print('Bonus: $%s' %(friend_bonus))
print('-----------------------')
#%%

# #Choose whether to open trial sheets or not
# open_or_not = input('Would you like to open the raw data files for this subject? (y/n): ')

# if open_or_not == 'y':
    
