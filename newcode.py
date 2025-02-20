#import modules
from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random
import pandas as pd
from decimal import Decimal
import numpy as np
from psychopy.hardware import keyboard


kb = keyboard.Keyboard()

#parameters
DEBUG = False

frame_rate = 1
initial_fixation_dur = 4
final_fixation_dur = 10
instruct_dur = 3
decision_dur = 2  # Choices shown for 2 seconds
trial_dur = 5

#set keys that will be used as acceptabe responses
choiceKeys = ('1', '9', 'z','escape','left', 'right')

showreturnscreen = 1

#get subjID
if DEBUG:
    sub_id = 'test'
    session = 'new'
    screen = 'n'
else:
    startDlg = gui.Dlg(title="SM Task")
    startDlg.addField('Session:', choices=["new", "returning"])
    startDlg.show()
    session = startDlg.data[0]

    if session == 'returning':
        returnDlg = gui.Dlg(title="REDO: SM Task")
        returnDlg.addField('Participant ID:')
        returnDlg.addField('Full Screen? (Enter lowercase: y or n):')
        returnDlg.show()
        sub_id = returnDlg.data[0]
        screen = returnDlg.data[1]
    else:
        subjDlg = gui.Dlg(title="SM Task")
        subjDlg.addField('Participant ID:')
        subjDlg.addField('Full Screen? (Enter lowercase: y or n):')
        subjDlg.show()
        sub_id = subjDlg.data[0]
        screen = subjDlg.data[1]

#initialize paths
expdir = os.getcwd()
subdir = f"{expdir}/Participant_Images/{sub_id}"

if not os.path.exists(subdir):
    print(f"Error:Directory {subdir} does not exist!")
    core.quit()


choicetrials = f"{sub_id}_gambles.csv"
choicetrials_path = os.path.join(subdir,choicetrials)

photoshare_trials = f"{sub_id}_trials.csv"
photoshare_path = os.path.join(subdir,photoshare_trials)

if os.path.exists(choicetrials_path):
    print(f"Loading spreadsheet: {choicetrials_path}")
    df_gambles = pd.read_csv(choicetrials_path)  # Load spreadsheet
    print(df_gambles.head())  # Display first few rows for debugging
else:
    print(f"Error: Spreadsheet {photoshare_trials} not found in {subdir}")
    core.quit()

if os.path.exists(photoshare_path):
    print(f"Loading spreadsheet: {photoshare_path}")
    df_photoshare = pd.read_csv(photoshare_path)  # Load spreadsheet
    print(df_photoshare.head())  # Display first few rows for debugging}}}
else:
    print(f"Error: Spreadsheet {photoshare_trials} not found in {subdir}")
    core.quit()


#timing setup
globalClock = core.Clock()

#window setup
useFullScreen = (screen == 'y')
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",fullscr=useFullScreen, allowGUI=True, screen=0)

#define stimuli for partner match screen

waiting_text = visual.TextStim (win, text= "Please wait to be matched with a partner.", pos=(0,0), height = 1, wrapWidth=30)
matched_text = visual.TextStim (win, text= " ", pos=(0,10), height = 1, wrapWidth=30)
presstobegin_text = visual.TextStim (win, text= "Press space to begin.", pos=(0,-10), height = 1, wrapWidth=30)
    
# Define enlarged sizes for all visual elements **before** the loop
syncing_text = visual.TextStim(win=win, name='syncing_text',
        text='Syncing…',
        font='Open Sans',
        pos=(0, 2.4), draggable=False, height=0.96, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0)

text_0 = visual.TextStim(win=win, name='text_0',
        text='0%',
        font='Open Sans',
        pos=(0, -1.6), draggable=False, height=0.8, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0)

Transparent = visual.Rect(
        win=win, name='Transparent',
        width=(8, 0.8)[0], height=(8, 0.8)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.2,
        colorSpace='rgb', lineColor='white', fillColor=[0.0000, 0.0000, 0.0000],
        opacity=None, depth=-4.0, interpolate=True)

Loading_25 = visual.Rect(
        win=win, name='Loading_25',
        width=(2, 0.8)[0], height=(2, 0.8)[1],
        ori=0.0, pos=(-3, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)

text_25 = visual.TextStim(win=win, name='text_25',
        text='25%',
        font='Open Sans',
        pos=(0, -1.6), draggable=False, height=0.8, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0)

Loading_50 = visual.Rect(
        win=win, name='Loading_50',
        width=(4, 0.8)[0], height=(4, 0.8)[1],
        ori=0.0, pos=(-2, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-7.0, interpolate=True)

text_50 = visual.TextStim(win=win, name='text_50',
        text='50%',
        font='Open Sans',
        pos=(0, -1.6), draggable=False, height=0.8, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-8.0);

Loading_75 = visual.Rect(
        win=win, name='Loading_75',
        width=(6, 0.8)[0], height=(6, 0.8)[1],
        ori=0.0, pos=(-1, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-9.0, interpolate=True)

text_75 = visual.TextStim(win=win, name='text_75',
        text='75%',
        font='Open Sans',
        pos=(0, -1.6), draggable=False, height=0.8, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-10.0)

Loading_100 = visual.Rect(
        win=win, name='Loading_100',
        width=(8, 0.8)[0], height=(8, 0.8)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-11.0, interpolate=True)

text_100 = visual.TextStim(win=win, name='text_100',
        text='100%',
        font='Open Sans',
        pos=(0, -1.6), draggable=False, height=0.8, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-12.0)

#define stimuli for photo share screen

photoshare_toptext = visual.TextStim(win, text= "Your photo is now being shared.", pos=(0,10), height = 1, wrapWidth=None)
photoshare_bottomtext = visual.TextStim(win, text= "Please wait for feedback.", pos=(0,-8), height = 1, wrapWidth=None)
feedback_text = visual.TextStim(win, text= "", pos=(0,10), height = 1, wrapWidth=None)

#stimuli for emotion1 ratings
emotion1_slider = visual.Slider(win=win, name='slider1',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion1question_text = visual.TextStim(win=win, name='emotion1question_text',
    text='Please rate the extent to which you feel happy. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#emotion 2 slider
emotion2_slider = visual.Slider(win=win, name='slider2',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion2question_text = visual.TextStim(win=win, name='emotion2question_text',
    text='Please rate the extent to which you feel emotion2. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#emotion3
emotion3_slider = visual.Slider(win=win, name='slider3',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion3question_text = visual.TextStim(win=win, name='emotion3question_text',
    text='Please rate the extent to which you feel emotion3. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#emotion 4
#stimuli for emotion1 ratings
emotion4_slider = visual.Slider(win=win, name='slider4',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion4question_text = visual.TextStim(win=win, name='emotion4question_text',
    text='Please rate the extent to which you feel emotion4. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#emotion5
#stimuli for emotion1 ratings
emotion5_slider = visual.Slider(win=win, name='slider5',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion5question_text = visual.TextStim(win=win, name='emotion5question_text',
    text='Please rate the extent to which you feel emotion5. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#stimuli for emotion6 ratings
emotion6_slider = visual.Slider(win=win, name='slider6',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

emotion6question_text = visual.TextStim(win=win, name='emotion6question_text',
    text='Please rate the extent to which you feel emotion6. \n\n Use your left and right arrows to move the arrow to your desired rating.',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

emotioncontinue_text = visual.TextStim(win=win, name='emotioncontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

displayrating_text = visual.TextStim(win=win, name='displayrating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

#salience rating screen
salience_slider = visual.Slider(win=win, name='salience_slider',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('Not at all', '', '', '', '', 'A lot'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

saliencequestion_text = visual.TextStim(win=win, name='saliencequestion_text',
    text='',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

saliencecontinue_text = visual.TextStim(win=win, name='saliencecontinue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

salienceavatar_image = visual.ImageStim(
    win=win,
    name='salienceavatar_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), draggable=False, size=(0.3, 0.55),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

displaysaliencerating_text = visual.TextStim(win=win, name='displaysaliencerating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)

# Define stimuli for gamble screens
top_box = visual.Rect(win, width=9.0, height=7.0, pos=(-10, 5),
                      lineWidth=5, lineColor='white', fillColor='black')
top_text = visual.TextStim(win, text="", pos=[-10, 5], height=1)

probability_text = visual.TextStim(win, text='', pos = [-10, 10.5], height =1)

bottom_box = visual.Rect(win, width=9.0, height=7.0, pos=(-10, -5),
                         lineWidth=5, lineColor='white', fillColor='black')
bottom_text = visual.TextStim(win, text="$0", pos=[-10, -5], height=1)

certain_box = visual.Rect(win, width=9.0, height=7.0, pos=(10, 0),
                          lineWidth=5, lineColor='white', fillColor='black')
certain_text = visual.TextStim(win, text="", pos=(10, 0), height=1)

cue = visual.TextStim(win, text="Make your choice", pos=(0, 10.5), height=1)

routine_clock = core.Clock()  # Initialize the clock

# Emotion Rating Screen
routine_clock.reset()  # Reset the clock before entering the loop
emotion1_slider.reset()  # Ensure slider starts fresh

# Reset the slider position
emotions = [
    {"name": "happy", "slider": emotion1_slider, "question": emotion1question_text},
    {"name": "emotion2", "slider": emotion2_slider, "question": emotion2question_text},
    {"name": "emotion3", "slider": emotion3_slider, "question": emotion3question_text},
    {"name": "emotion4", "slider": emotion4_slider, "question": emotion4question_text},
    {"name": "emotion5", "slider": emotion5_slider, "question": emotion5question_text},
    {"name": "emotion6", "slider": emotion6_slider, "question": emotion6question_text},]

# Set slider constraints
slider_min = 0
slider_max = 5

# Iterate through each emotion rating screen
for emotion in emotions:
    emotion_slider = emotion["slider"]
    emotion_question_text = emotion["question"]
    
    # Reset the slider before use
    emotion_slider.markerPos = 2.5  
    rating_selected = False  

    # Clear previous key events
    event.clearEvents('keyboard')

    while not rating_selected:  # Keep the screen up until space is pressed
        keys = event.getKeys()  # Get key presses
        displayrating_text.setText(round(emotion_slider.getMarkerPos(), 1))  # Update display

        if keys:  # Process keys only if pressed
            if 'left' in keys:
                emotion_slider.markerPos = max(slider_min, emotion_slider.markerPos - 0.1)
                displayrating_text.setText(round(emotion_slider.getMarkerPos(), 1))
            elif 'right' in keys:
                emotion_slider.markerPos = min(slider_max, emotion_slider.markerPos + 0.1)
                displayrating_text.setText(round(emotion_slider.getMarkerPos(), 1))
            elif 'escape' in keys:
                win.close()
                core.quit()
            elif 'space' in keys:
                rating_selected = True  # Exit the loop

        # Draw all components before flipping
        emotion_slider.draw()
        emotion_question_text.draw()
        displayrating_text.draw()
        emotioncontinue_text.draw()
        win.flip()  # Refresh the screen after updating everything





#match with partner and photo share

for index, row in df_photoshare.iterrows():
    if row['TrialNumber'] not in [1, 31, 61, 91]: # establishes two blocks per 30 trials
        continueRoutine = False # if not trial 31 or 63, skip routine completely

    if 'escape' in event.getKeys():
        win.close()
        core.quit()

    charlie_emoji = os.path.join(expdir, "Task_Images", "nerdemoji_nobackground.png")
    riley_emoji = os.path.join(expdir, "Task_Images", "huggingemoji.png")
    sam_emoji = os.path.join(expdir, "Task_Images", "smilingemoji.png")
    alex_emoji = os.path.join(expdir, "Task_Images", "sunglassemoji_nobackground.png")

    partner_name = row['Partner'] # got partner name from the spreadhseet
    matched_text = 'You have matched with' + " " + str(partner_name) + "!"
    
    if partner_name == 'Charlie':
        partneravatar= charlie_emoji
    elif partner_name == 'Riley':
        partneravatar= riley_emoji
    elif partner_name == 'Alex':
        partneravatar= alex_emoji
    elif partner_name =='Sam':
        partneravatar= sam_emoji

    # Create stimuli
    partner_avatar_stim = visual.ImageStim(win, image=partneravatar, size=(5, 5), pos=(0, 2))
    matched_text_stim = visual.TextStim(win, text=matched_text, pos=(0, 7), height=1, color='white', wrapWidth=30)

     # Start trial
trial_onset = globalClock.getTime()


# **Step 1: Display Waiting Text for 3 sec**
while routine_clock.getTime() < 3:
    waiting_text.draw()
    win.flip()

# **Step 2: Start Syncing + Transparent**
routine_clock.reset()  # Reset timer for syncing phase
while routine_clock.getTime() < 6.25:
    syncing_text.draw()  # Syncing stays the full 9.25 sec
    Transparent.draw()  # Transparent stays for 6.25 sec
    
    # **Text 0 (appears at 3 sec, disappears after 1.25 sec)**
    if routine_clock.getTime() < 1.25:
        text_0.draw()
    
    # **Text 25 + Loading 25 (appears at 4.25 sec, disappears after 1.25 sec)**
    elif 1.25 <= routine_clock.getTime() < 2.5:
        Loading_25.draw()
        text_25.draw()
    
    # **Text 50 + Loading 50 (appears at 5.5 sec, disappears after 1.25 sec)**
    elif 2.5 <= routine_clock.getTime() < 3.75:
        Loading_50.draw()
        text_50.draw()

    # **Text 75 + Loading 75 (appears at 6.75 sec, disappears after 1.25 sec)**
    elif 3.75 <= routine_clock.getTime() < 5:
        Loading_75.draw()
        text_75.draw()

    # **Text 100 + Loading 100 (appears at 8 sec, disappears after 1.25 sec)**
    elif 5 <= routine_clock.getTime() < 6.25:
        Loading_100.draw()
        text_100.draw()

    win.flip()

# **Step 3: Show Matched Text and Partner Avatar**
win.flip()

matched_text_stim.draw()
partner_avatar_stim.draw()
presstobegin_text.draw()
win.flip()

#wait for spacebar press before proceeding
event.waitKeys(keyList=['space'])


#get salience rating

# Set slider constraints
slider_min = 0
slider_max = 5

# Clear previous key events
salienceratingtext = (f'How likely are you to share photos with {partner_name} in the future? \n\n Use your left and right arrows to move the arrow to your desired rating.' )
event.clearEvents('keyboard')
salience_slider.markerPos = 2.5
saliencequestion_text.setText(salienceratingtext)
rating_selected = False  # Reset before the salience rating loop

while not rating_selected:  # Keep the screen up until space is pressed
        keys = event.getKeys()  # Get key presses
        displaysaliencerating_text.setText(round(salience_slider.getMarkerPos(), 1))  # Update display

        if keys:  # Process keys only if pressed
            if 'left' in keys:
                salience_slider.markerPos = max(slider_min, salience_slider.markerPos - 0.1)
                displaysaliencerating_text.setText(round(salience_slider.getMarkerPos(), 1))
            elif 'right' in keys:
                salience_slider.markerPos = min(slider_max, salience_slider.markerPos + 0.1)
                displaysaliencerating_text.setText(round(salience_slider.getMarkerPos(), 1))
            elif 'escape' in keys:
                win.close()
                core.quit()
            elif 'space' in keys:
                rating_selected = True  # Exit the loop

        # Draw all components before flipping
        salience_slider.draw()
        saliencequestion_text.draw()
        displaysaliencerating_text.draw()
        saliencecontinue_text.draw()
        partner_avatar_stim.draw()
        win.flip()  # Refresh the screen after updating everything


#iterate through photo sharing and feedback screen
for index, row in df_photoshare.iterrows():
    if 'escape' in event.getKeys():
        win.close()
        core.quit()

    partner_name = row['Partner'] # got partner name from the spreadhseet
    
    
    photo_file = row['Photos']  # Get photo path from the spreadsheet
    feedback = row['Feedback'] # get feedback text from the spreadsheet
    # Extract values from the spreadsheet
    feedback_text = str(row['Partner']) + " " + str(row['Feedback']) + ' ' + 'your photo.' 

    # Ensure there are no leading slashes to avoid absolute path issues
    photo_file = photo_file.lstrip(os.sep)
    posfeedback_image = os.path.join(expdir, "Task_Images", "thumbsup.png")
    negfeedback_image = os.path.join(expdir, "Task_Images", "thumbsdown.png")

    # Construct full path by joining the experiment directory with the spreadsheet path
    full_photo_path = os.path.normpath(os.path.join(expdir, photo_file))

    if not os.path.exists(full_photo_path):
        print(f"Subdir: {subdir}")
        print(f"Photo File: {photo_file}")
        print(f"Error: Photo {full_photo_path} not found! Skipping trial {index}.")
        continue  # Skip if missing

    display_duration = row['FeedbackWait']  # Column name from your CSV

    # Display the photo
    photo_displayed = visual.ImageStim(win, image=full_photo_path, size=(10, 10), pos=(0, 0))
    
    photoshare_toptext.draw()
    photoshare_bottomtext.draw()
    photo_displayed.draw()
    win.flip()
    core.wait(display_duration)  # Show for randomized amounts of time

    win.flip()
    
    
    # Determine which feedback image to use
    if 'not' in str(row['Feedback']).lower():  # Convert to string & lowercase for safety
        feedbackimage = negfeedback_image
    else:
        feedbackimage = posfeedback_image

    #display the feedback
    feedback_stim = visual.TextStim(win, text=feedback_text, pos=(0, 5), height=1, color='white')
    feedback_image_stim = visual.ImageStim(win, image=feedbackimage, size=(5, 5), pos=(0, -3))

    # **Step 5: Show Feedback Text and Image**
    feedback_stim.draw()
    feedback_image_stim.draw()
    win.flip()
    core.wait(2)  # Show feedback for 2 seconds


# Iterate over trials
for index, row in df_gambles.iterrows():
    # Reset colors each trial
    top_text.setColor('white')
    bottom_text.setColor('white')
    certain_text.setColor('white')
    probability_text.setColor('white')

    # Extract values from the spreadsheet
    probability_text.text = str(row['win_probability'])
    top_text.text = str(row['risky_gain'])
    certain_text.text = str(row['certain'])

    # Start trial
    trial_onset = globalClock.getTime()

    # Step 1: Display Choices for 2 Seconds
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    probability_text.draw()
    win.flip()
    core.wait(2)  # Show choices for 2 seconds

    # Step 2: Show "Make Your Choice" and Wait for Response
    cue.draw()
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    probability_text.draw()
    win.flip()

    cue_onset = globalClock.getTime()

    event.clearEvents()  # Clear buffer before capturing input
    resp = None
    response_timer = core.Clock()  # Start response timer

    while response_timer.getTime() < decision_dur:
        resp = event.getKeys(keyList=choiceKeys)
        if resp:
            resp = resp[0]  # Get first key press
            break  # Exit loop when response is received

    # Step 3: Process Response and Provide Feedback
    if resp:
        print(f"Captured response: {resp}")

        if resp == 'z':  # Quit if 'z' is pressed
            win.close()
            core.quit()

        elif resp == '1':  # Risky option selected
            top_text.setColor('green')
            probability_text.setColor('green')
            bottom_text.setColor('green')

        elif resp == '9':  # Certain option selected
            certain_text.setColor('green')

    else:  # No response detected, show red
        top_text.setColor('red')
        bottom_text.setColor('red')
        certain_text.setColor('red')
        probability_text.setColor('red')

    # Redraw with updated colors
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    probability_text.draw()
    cue.draw()
    win.flip()
    core.wait(1)  # Show feedback for 1 second

# Close the experiment
win.close()
core.quit()