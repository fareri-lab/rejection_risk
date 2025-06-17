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
        labels=('0','1(Not at all)', '2', '3', '4', '5 (A lot)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=('0','1(Not at all)', '2', '3', '4', '5 (A lot)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=(['0','1(Not at all)', '2', '3', '4', '5 (A lot)']), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=('0','1(Not at all)', '2', '3', '4', '5 (A lot)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=('0','1(Not at all)', '2', '3', '4', '5 (A lot)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=('0','1(Not at all)', '2', '3', '4', '5 (A lot)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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
        labels=('0 (Not Likely)', '1', '2', '3', '4', ' 5(Very Likely)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
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

emotions = [
    {"name": "happy", "slider": emotion1_slider, "question": emotion1question_text},
    {"name": "emotion2", "slider": emotion2_slider, "question": emotion2question_text},
    {"name": "emotion3", "slider": emotion3_slider, "question": emotion3question_text},
    {"name": "emotion4", "slider": emotion4_slider, "question": emotion4question_text},
    {"name": "emotion5", "slider": emotion5_slider, "question": emotion5question_text},
    {"name": "emotion6", "slider": emotion6_slider, "question": emotion6question_text},]

def partner_match_with_loading(win, partner_name, expdir):
    """
    Displays a loading bar before showing the partner match screen.

    Parameters:
        win (visual.Window): The PsychoPy window where stimuli will be displayed.
        partner_name (str): The name of the partner from the trial data.
        expdir (str): The experiment directory where images are stored.
    """
    
    # Define emoji image paths
    emoji_paths = {
        'Charlie': os.path.join(expdir, "Task_Images", "nerdemoji_nobackground.png"),
        'Riley': os.path.join(expdir, "Task_Images", "huggingemoji.png"),
        'Alex': os.path.join(expdir, "Task_Images", "sunglassemoji_nobackground.png"),
        'Sam': os.path.join(expdir, "Task_Images", "smilingemoji.png")
    }

    # Get partner avatar image path
    partneravatar = emoji_paths.get(partner_name, os.path.join(expdir, "Task_Images", "defaultemoji.png"))

    # Create "Syncing..." text
    syncing_text = visual.TextStim(win, text='Syncing…', pos=(0, 2.4), height=0.96, color='white')

    # Create loading percentage text
    percentage_texts = [
        visual.TextStim(win, text='0%', pos=(0, -1.6), height=0.8, color='white'),
        visual.TextStim(win, text='25%', pos=(0, -1.6), height=0.8, color='white'),
        visual.TextStim(win, text='50%', pos=(0, -1.6), height=0.8, color='white'),
        visual.TextStim(win, text='75%', pos=(0, -1.6), height=0.8, color='white'),
        visual.TextStim(win, text='100%', pos=(0, -1.6), height=0.8, color='white')
    ]

    # Create loading bar components
    loading_bars = [
        visual.Rect(win, width=2, height=0.8, pos=(-3, 0), fillColor='white'),
        visual.Rect(win, width=4, height=0.8, pos=(-2, 0), fillColor='white'),
        visual.Rect(win, width=6, height=0.8, pos=(-1, 0), fillColor='white'),
        visual.Rect(win, width=8, height=0.8, pos=(0, 0), fillColor='white')
    ]

    # **Step 1: Show Loading Animation**
    routine_clock = core.Clock()
    while routine_clock.getTime() < 6.25:  # Total duration: 6.25 seconds

        syncing_text.draw()  # Always show "Syncing..."

        # Show different stages of loading at correct times
        time_elapsed = routine_clock.getTime()
        if time_elapsed < 1.25:
            percentage_texts[0].draw()
        elif 1.25 <= time_elapsed < 2.5:
            loading_bars[0].draw()
            percentage_texts[1].draw()
        elif 2.5 <= time_elapsed < 3.75:
            loading_bars[1].draw()
            percentage_texts[2].draw()
        elif 3.75 <= time_elapsed < 5:
            loading_bars[2].draw()
            percentage_texts[3].draw()
        elif 5 <= time_elapsed < 6.25:
            loading_bars[3].draw()
            percentage_texts[4].draw()

        win.flip()  # Update the screen

    # **Step 2: Display Matched Partner Screen**
    matched_text = f"You have matched with {partner_name}!"
    partner_avatar_stim = visual.ImageStim(win, image=partneravatar, size=(5, 5), pos=(0, 2))
    matched_text_stim = visual.TextStim(win, text=matched_text, pos=(0, 7), height=1, color='white')
    presstobegin_text = visual.TextStim(win, text="Press space to begin.", pos=(0, -7), height=1, color='white')

    matched_text_stim.draw()
    partner_avatar_stim.draw()
    presstobegin_text.draw()
    win.flip()

    # Wait for spacebar press before proceeding
    event.waitKeys(keyList=['space'])

def display_emotion_ratings(win, emotions, slider_min=0, slider_max=5):
    """
    Displays emotion rating screens one at a time, allowing the user to adjust sliders.

    Parameters:
        win (visual.Window): The PsychoPy window object.
        emotions (list): A list of dictionaries, each containing:
            - "name" (str): Name of the emotion.
            - "slider" (visual.Slider): The slider object for rating.
            - "question" (visual.TextStim): The question text associated with the slider.
        slider_min (int, optional): Minimum slider value. Default is 0.
        slider_max (int, optional): Maximum slider value. Default is 5.
    """
    routine_clock.reset()  # Reset the clock before entering the loop

    # Set slider constraints
    slider_min = 0
    slider_max = 5
    emotion_ratings = {}

    # Iterate through each emotion rating screen
    for emotion in emotions:
        emotion_slider = emotion["slider"]
        emotion_question_text = emotion["question"]
        
        # Reset the slider before use
        emotion_slider.reset()  # Ensure slider starts fresh
        emotion_slider.markerPos = 2.5  
        rating_selected = False 

        # Draw all components before flipping
        emotion_slider.draw()
        emotion_question_text.draw()
        displayrating_text.draw()
        emotioncontinue_text.draw()
        win.flip()  # Refresh the screen after updating everything

            # Clear previous key events
        kb.clearEvents()

        while not rating_selected:  # Keep the screen up until space is pressed
            keys = event.getKeys()  # Get key presses
            displayrating_text.setText(round(emotion_slider.getMarkerPos(), 1))  # Update display

            if keys:  # Process keys only if pressed
                for key in keys:
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

        #store selected rating
        emotion_ratings[emotion["name"]] = round(emotion_slider.getMarkerPos(), 1)
        
    return emotion_ratings

def photo_share_screen(win,row):
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
    continue_text = visual.TextStim(win, text="Press space to continue.", pos=(0, -8), height=1, color='white')


    #Show Feedback Text and Image**
    feedback_stim.draw()
    feedback_image_stim.draw()
    continue_text.draw()
    win.flip()

    #Wait for Space Key and Record Response Time**
    response_timer = core.Clock()  # Start timing when the message appears
    event.clearEvents()
    keys = event.waitKeys(keyList=['space', 'escape'], timeStamped=response_timer)

    photo_response_time = None
    # If escape is pressed, exit the experiment
    for key, timestamp in keys:
        if key == 'escape':
            win.close()
            core.quit()
        elif key == 'space':
            photo_response_time = timestamp  # Capture response time

    return photo_response_time  # ✅ Return the time taken to press space
    

def gamble_screen(win,row):
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
    gamble_choice = None
    response_timer = core.Clock()  # Start response timer

    while response_timer.getTime() < decision_dur:
        resp = event.getKeys(keyList=choiceKeys)
        if resp:
            resp = resp[0]  # Get first key press
            break  # Exit loop when response is received
    
    gamble_response_time = None
    # Step 3: Process Response and Provide Feedback
    if resp:
        print(f"Captured response: {resp}")

        if resp == 'z':  # Quit if 'z' is pressed
            win.close()
            core.quit()

        elif resp == '1':  # Risky option selected
            gamble_choice = 1
            top_text.setColor('green')
            probability_text.setColor('green')
            bottom_text.setColor('green')

        elif resp == '9':  # Certain option selected
            gamble_choice = 0
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
    core.wait(1)  # Show feedback for 1 
    
    gamble_response_time = response_timer.getTime() if resp else None
    return gamble_response_time, gamble_choice  # Now correctly coded as 1 (Risky) or 0 (Certain)

def salience_rating(win, partner_avatar_stim,partner_name):
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

    # ✅ Return the selected rating  
    return round(salience_slider.getMarkerPos(), 1)

# Define a list to store trial data
trials_per_block = 30  # Each block has 30 trials
experiment_data = []

# Define the output directory for data storage
data_dir = os.path.join(expdir, "data")

# Ensure the data directory exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the output file path
output_file = os.path.join(data_dir, f"{sub_id}_data.csv")

def save_data():
    """ Save the collected experiment data to CSV. """
    if experiment_data:  
        df_output = pd.DataFrame(experiment_data)
        df_output.to_csv(output_file, index=False)
        print(f"DEBUG: Experiment data saved to {output_file}") 

try:
    choice_index = 0  # Track which gamble choice we're on

    for block_start in range(0, len(df_photoshare), trials_per_block):
        block = df_photoshare.iloc[block_start:block_start + trials_per_block]
        
        # **Partner Match on First Trials of Blocks**
        first_trial = block.iloc[0]['TrialNumber']
        if first_trial in [1, 31, 61, 91]:
            print(f"DEBUG: Partner Match on Trial {first_trial}")
            partner_match_with_loading(win, block.iloc[0]['Partner'], expdir)

        # **Emotion Rating at the Start of Each Block**
        if first_trial in [1, 30, 60, 90, 120]:
            print(f"DEBUG: Emotion Ratings on Trial {first_trial}")
            emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
            experiment_data.append({"TrialNumber": first_trial, **emotion_ratings})

        # ✅ **Run Three 5-Photo, 5-Gamble Sequences**
        for cycle in range(3):  
            photo_batch_start = cycle * 5
            gamble_batch_start = choice_index  # Track where we are in gamble trials

            # **Show 5 Photo Shares**
            batch_photos = block.iloc[photo_batch_start:photo_batch_start + 5]
            for _, photo_row in batch_photos.iterrows():
                trial = photo_row['TrialNumber']
                print(f"DEBUG: Photo Share Trial {trial}")
                response_time_photo = photo_share_screen(win, photo_row)
                experiment_data.append({
                    "TrialNumber": trial,
                    "Task": "PhotoShare",
                    "PhotoResponseTime": response_time_photo
                })

            # **Show 5 Gambles**
            batch_gambles = df_gambles.iloc[gamble_batch_start:gamble_batch_start + 5]
            for _, gamble_row in batch_gambles.iterrows():
                trial = gamble_row['ChoiceNumber']
                print(f"DEBUG: Gamble Trial {trial}")
                response_time_gamble, gamble_choice = gamble_screen(win, gamble_row)

                experiment_data.append({
                    "TrialNumber": trial,
                    "Task": "Gamble",
                    "ChoiceNumber": gamble_row['ChoiceNumber'],
                    "GambleResponseTime": response_time_gamble,
                    "GambleChoice": gamble_choice,
                    "SelectedPrice": gamble_row["risky_gain"] if gamble_choice == 1 else gamble_row["certain"],
                    "WinProbability": gamble_row["win_probability"] if gamble_choice == 1 else None
                })

            choice_index += 5  # Move to the next set of gambles

        # ✅ **Midway Emotion Rating After 15 Trials**
        midway_trial = block.iloc[14]['TrialNumber']
        if midway_trial in [15, 45, 75, 105]:
            print(f"DEBUG: Midway Emotion Rating on Trial {midway_trial}")
            emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
            experiment_data.append({"TrialNumber": midway_trial, **emotion_ratings})

        # ✅ **Now Run the Second Half (Trials 16-30)**
        for batch_start in range(15, 30, 5):
            batch_photos = block.iloc[batch_start:batch_start + 5]  # 5 photo trials
            batch_gambles = df_gambles.iloc[choice_index:choice_index + 5]  # 5 gamble trials

            # **Show 5 Photo Shares**
            for _, photo_row in batch_photos.iterrows():
                trial = photo_row['TrialNumber']
                print(f"DEBUG: Photo Share Trial {trial}")
                response_time_photo = photo_share_screen(win, photo_row)
                experiment_data.append({
                    "TrialNumber": trial,
                    "Task": "PhotoShare",
                    "PhotoResponseTime": response_time_photo
                })

            # **Show 5 Gambles**
            for _, gamble_row in batch_gambles.iterrows():
                trial = gamble_row['ChoiceNumber']
                print(f"DEBUG: Gamble Trial {trial}")
                response_time_gamble, gamble_choice = gamble_screen(win, gamble_row)

                experiment_data.append({
                    "TrialNumber": trial,
                    "Task": "Gamble",
                    "ChoiceNumber": gamble_row['ChoiceNumber'],
                    "GambleResponseTime": response_time_gamble,
                    "GambleChoice": gamble_choice,
                    "SelectedPrice": gamble_row["risky_gain"] if gamble_choice == 1 else gamble_row["certain"],
                    "WinProbability": gamble_row["win_probability"] if gamble_choice == 1 else None
                })

            choice_index += 5  # Move to the next set of gambles

        # ✅ **Final Emotion + Salience Ratings**
        last_trial = block.iloc[-1]['TrialNumber']
        if last_trial in [30, 60, 90, 120]:
            print(f"DEBUG: Final Emotion & Salience Ratings on Trial {last_trial}")
            emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
            salience_rating_value = salience_rating(win, salienceavatar_image, block.iloc[-1]['Partner'])
            experiment_data.append({
                "TrialNumber": last_trial,
                **emotion_ratings,
                "SalienceRating": salience_rating_value
            })

        # **Save Data After Each Block**
        save_data()

except KeyboardInterrupt:
    print("Experiment interrupted. Saving data...")
    save_data()

except Exception as e:
    print(f"ERROR: {e}\nSaving collected data before exiting.")
    save_data()
    sys.exit(1)

# **Final Save Before Exit**
save_data()

# Close PsychoPy window
win.close()
core.quit()















# # Loop through the trials
# # Total trials and block settings
# total_trials = 120
# trials_per_block = 30
# photo_gamble_cycle = 10  # 5 Photo + 5 Gamble = 10 trials per cycle
# num_cycles_before_mid_emotion = 3  # 3 cycles (15 trials) before mid-block Emotion Ratings
# num_cycles_after_mid_emotion = 3  # 3 cycles (15 trials) after mid-block Emotion Ratings

# # Initialize an empty list to store trial data
# experiment_data = []

# # Loop through the trials
# for trial in range(1, total_trials + 1):

#     print(f"DEBUG: Starting Trial {trial}")
    
#     # Identify which block this trial belongs to
#     block_number = (trial - 1) // trials_per_block + 1

#     # Create a dictionary for trial data with empty values by default
#     trial_data = {
#         "TrialNumber": trial,
#         "Block": block_number,
#         "Partner": None,
#         "Condition": None,
#         "Feedback": None,
#         "ResponseTime": None,
#         "GambleChoice": None,
#         "GambleProbability": None,
#         "GamblePrice": None,
#         "NonGamblePrice": None,
#         "SelectedPrice": None,
#         "Emotion1": None,
#         "Emotion2": None,
#         "Emotion3": None,
#         "Emotion4": None,
#         "Emotion5": None,
#         "Emotion6": None,
#         "SalienceRating": None
#     }

#     # **Partner Match on the first trial of each block**
#     if trial in [1, 31, 61, 91]:  
#         print(f"DEBUG: Partner Match on Trial {trial}")
#         row = df_photoshare.iloc[trial - 1]
#         partner_name = row['Partner']
#         trial_data["Partner"] = partner_name

#         partner_match_with_loading(win, partner_name, expdir)

#         # **Emotion Ratings immediately after Partner Match**
#         print(f"DEBUG: Emotion Ratings on Trial {trial}")
#         emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
        
#         if emotion_ratings:  # Check if valid data is returned
#             for i, rating in enumerate(emotion_ratings.values()):
#                 trial_data[f"Emotion{i+1}"] = rating

#     # **Determine Photo Share or Gamble Trial**
#     cycle_position = (trial - 1) % trials_per_block  
#     cycle_within_set = cycle_position % photo_gamble_cycle  

#     if cycle_position < 15 or (15 < cycle_position < 30):  
#         if cycle_within_set < 5:  
#             print(f"DEBUG: Photo Share Trial {trial}")
#             row = df_photoshare.iloc[(trial - 1) % len(df_photoshare)]
#             trial_data["Partner"] = row['Partner']
#             trial_data["Feedback"] = row['Feedback']
#             photo_share_screen(win)
#         else:  
#             print(f"DEBUG: Gamble Trial {trial}")
#             row = df_gambles.iloc[(trial - 1) % len(df_gambles)]
#             response_time, gamble_choice = gamble_screen(win)

#             # Store gamble data
#             trial_data["ResponseTime"] = response_time
#             trial_data["GambleChoice"] = gamble_choice  # Now correctly coded as 1 (Risky) or 0 (Certain)
#             trial_data["GambleProbability"] = row["win_probability"]
#             trial_data["GamblePrice"] = row["risky_gain"]
#             trial_data["NonGamblePrice"] = row["certain"]
#             trial_data["SelectedPrice"] = row["risky_gain"] if gamble_choice == 1 else row["certain"]

#     # **Mid-Block Emotion Ratings after 15 trials (Trial 15, 45, 75, 105)**
#     if cycle_position == (num_cycles_before_mid_emotion * photo_gamble_cycle - 1):  
#         print(f"DEBUG: Emotion Rating on Trial {trial}")
#         emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)

#         if emotion_ratings:  # Check if valid data is returned
#             for i, rating in enumerate(emotion_ratings.values()):
#                 trial_data[f"Emotion{i+1}"] = rating

#     # **Final Emotion + Salience Ratings at the end of the block (Trial 30, 60, 90, 120)**
#     if cycle_position == (trials_per_block - 1):  
#         print(f"DEBUG: Emotion & Salience Rating on Trial {trial}")
#         emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)

#         if emotion_ratings:  # Check if valid data is returned
#             for i, rating in enumerate(emotion_ratings.values()):
#                 trial_data[f"Emotion{i+1}"] = rating

#         print(f"DEBUG: Salience Rating on Trial {trial}")
#         trial_data["SalienceRating"] = salience_rating(win, salienceavatar_image)

#     # **Append trial data to experiment_data list**
#     experiment_data.append(trial_data)

# # **Saving Data**
# # Define the output directory for data storage
# data_dir = os.path.join(expdir, "data")

# # Ensure the data directory exists; if not, create it
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)

# # Define the output file path in the data folder
# output_file = os.path.join(data_dir, f"{sub_id}_data.csv")

# # Convert list of dictionaries into a DataFrame
# df_output = pd.DataFrame(experiment_data)

# # Save to CSV in the correct directory
# df_output.to_csv(output_file, index=False)
# print(f"DEBUG: Experiment data saved to {output_file}")

# # Close the experiment window after all trials
# win.close()
# core.quit()



# # Loop through the trials
# for trial in range(1, total_trials + 1):

#     print(f"DEBUG: Starting Trial {trial}")

#     # **Partner Match on the first trial of each block, THEN Emotion Ratings**
#     if trial in [1, 31, 61, 91]:  
#         print(f"DEBUG: Partner Match on Trial {trial}")
#         row = df_photoshare.iloc[trial - 1]
#         partner_name = row['Partner']
        
#         # **Show Partner Match first**
#         partner_match_with_loading(win, partner_name, expdir)

#         # **Then show Emotion Ratings**
#         print(f"DEBUG: Emotion Ratings on Trial {trial}")
#         display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)

#     # **Determine Photo Share or Gamble Trial**
#     cycle_position = (trial - 1) % trials_per_block  # Position within the block
#     cycle_within_set = cycle_position % photo_gamble_cycle  # Position within the 10-trial cycle

#     if cycle_position < 15 or (15 < cycle_position < 30):  # Before AND after mid-block emotion ratings
#         if cycle_within_set < 5:  # First 5 trials → Photo Share
#             print(f"DEBUG: Photo Share Trial {trial}")
#             row = df_photoshare.iloc[(trial - 1) % len(df_photoshare)]
#             photo_share_screen(win)
#         else:  # Next 5 trials → Gamble
#             print(f"DEBUG: Gamble Trial {trial}")
#             row = df_gambles.iloc[(trial - 1) % len(df_gambles)]
#             gamble_screen(win)

#     # **Mid-Block Emotion Ratings after 15 trials (Trial 15, 45, 75, 105)**
#     if cycle_position == (num_cycles_before_mid_emotion * photo_gamble_cycle - 1):  # Trial 15, 45, 75, 105
#         print(f"DEBUG: Emotion Rating on Trial {trial}")
#         display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)

#     # **Final Emotion + Salience Ratings at the end of the block (Trial 30, 60, 90, 120)**
#     if cycle_position == (trials_per_block - 1):  # Trial 30, 60, 90, 120
#         print(f"DEBUG: Emotion & Salience Rating on Trial {trial}")
#         display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
#         salience_rating(win, salienceavatar_image)  # Display Salience Rating

# print("DEBUG: Experiment Completed.")

# # Close the experiment window after all trials
# win.close()
# core.quit()









# # Loop through trials
# for index, row in df_photoshare.iterrows():
#     if choiceKeys = 'z'
#         core.quit()
#     # Only run this on specific trial numbers (partner match trials)
#     if row['TrialNumber'] in [1, 31, 61, 91]:  
        
#         # Extract partner name from the trial data
#         partner_name = row['Partner']
        
#         # Call the function to display loading and partner match screen
#         partner_match_with_loading(win, partner_name, expdir)

#         display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)

#     if row["TrialNumber"] in range(1,120):

#         photo_share_screen(win)














