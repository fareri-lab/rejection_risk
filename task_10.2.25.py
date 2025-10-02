#import modules


from psychopy import visual, core, event, gui, data, sound, logging
from psychopy.hardware import keyboard

import os
import sys
import csv
from datetime import datetime
import random
import pandas as pd
from decimal import Decimal
import numpy as np
import webbrowser



kb = keyboard.Keyboard()

experiment_data = []
pending_photo_data = []
photo_trial_num = 1
gamble_trial_num = 1


def save_and_quit():
    df = pd.DataFrame(experiment_data)
    filename = f"data/{sub_id}_taskdata_.csv"
    #{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    win.close()
    core.quit()


#parameters
DEBUG = False

frame_rate = 1
initial_fixation_dur = 4
final_fixation_dur = 10
instruct_dur = 3
decision_dur = 2  # Choices shown for 2 seconds
trial_dur = 5

#set keys that will be used as acceptabe responses
choiceKeys = ('c', 'n', 'z','escape','left', 'right')

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
    text='Please rate the extent to which you feel sad. \n\n Use your left and right arrows to move the arrow to your desired rating.',
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
    text='Please rate the extent to which you feel afraid. \n\n Use your left and right arrows to move the arrow to your desired rating.',
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
    text='Please rate the extent to which you feel angry. \n\n Use your left and right arrows to move the arrow to your desired rating.',
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
    text='Please rate the extent to which you feel surprised. \n\n Use your left and right arrows to move the arrow to your desired rating.',
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
    text='Please rate the extent to which you feel disgusted. \n\n Use your left and right arrows to move the arrow to your desired rating.',
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

#future sharing rating screen
futuresharing_slider = visual.Slider(win=win, name='futuresharing_slider',
        startValue=999, size=(12.0, 0.8), pos=(0, -3.2), units=None,
        labels=('0 (Not Likely)', '1', '2', '3', '4', ' 5(Very Likely)'), ticks=(0,1, 2, 3, 4, 5), granularity=0.0,
        style='rating', styleTweaks=('labels45', 'triangleMarker'), opacity=None,
        labelColor='white', markerColor='cornflowerblue', lineColor='white', colorSpace='rgb',
        font='Open Sans', labelHeight=0.05, 
        flip=False, ori=0.0, depth=-5, readOnly=False)

futuresharing_question_text = visual.TextStim(win=win, name='futuresharing_question_text',
    text='',
    font='Open Sans',
    pos=(0, 4.8), draggable=False, height=1, wrapWidth=30, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0)

futuresharing_continue_text = visual.TextStim(win=win, name='futuresharing_continue_text',
    text='Press space to enter rating and continue.',
    font='Open Sans',
    pos=(0, -8), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0)

futuresharing_avatar_image = visual.ImageStim(
    win=win,
    name='futuresharing_avatar_image', 
    image='default.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.8),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)

display_futuresharing_rating_text = visual.TextStim(win=win, name='display_futuresharing_rating_text',
    text='',
    font='Open Sans',
    pos=(0, -5.2), draggable=False, height=1, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0)


emoji_paths = {
            'Charlie': os.path.join(expdir, "Task_Images", "nerdemoji_nobackground.png"),
            'Riley': os.path.join(expdir, "Task_Images", "huggingemoji.png"),
            'Alex': os.path.join(expdir, "Task_Images", "sunglassemoji_nobackground.png"),
            'Sam': os.path.join(expdir, "Task_Images", "smilingemoji.png")
        }
# Define stimuli for gamble screens
top_box = visual.Rect(win, width=9.0, height=7.0, pos=(-10, 5),
                      lineWidth=5, lineColor='white', fillColor='black')
top_text = visual.TextStim(win, text="", pos=[-10, 5], height=1)

#probability_text = visual.TextStim(win, text='', pos = [-10, 10.5], height =1)

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

    # Clear any lingering keypresses and wait for space
    event.clearEvents()
    keys = event.waitKeys(keyList=['space'])

    if 'escape' in keys:
        save_and_quit()
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
                        save_and_quit()
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
            save_and_quit()
        elif key == 'space':
            photo_response_time = timestamp  # Capture response time

    return photo_response_time  # ✅ Return the time taken to press space
    

def gamble_screen(win,row):
    # Reset colors each trial
    top_text.setColor('white')
    bottom_text.setColor('white')
    certain_text.setColor('white')
    #probability_text.setColor('white')

    # Extract values from the spreadsheet
    #probability_text.text = str(row['win_probability'])
    top_text.text = f"${row['risky_gain']}"
    certain_text.text = f"${row['certain']}"


    # Start trial
    trial_onset = globalClock.getTime()

    # Step 1: Display Choices for 2 Seconds
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    #probability_text.draw()
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
    #probability_text.draw()
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
            save_and_quit()

        elif resp == 'c':  # Risky option selected
            gamble_choice = 1
            top_text.setColor('orange')
           # probability_text.setColor('green')
            bottom_text.setColor('orange')

        elif resp == 'n':  # Certain option selected
            gamble_choice = 0
            certain_text.setColor('orange')

    else:  # No response detected, show red
        gamble_choice = 999
        top_text.setColor('gray')
        bottom_text.setColor('gray')
        certain_text.setColor('gray')
        #probability_text.setColor('red')

    # Redraw with updated colors
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    #probability_text.draw()
    cue.draw()
    win.flip()
    core.wait(1)  # Show feedback for 1 
    
    gamble_response_time = response_timer.getTime() if resp else None
    return gamble_response_time, gamble_choice  # Now correctly coded as 1 (Risky) or 0 (Certain)

def futuresharing_rating(win, partner_avatar_stim,partner_name):
    # Set slider constraints
    slider_min = 0
    slider_max = 5

    # Clear previous key events
    futuresharing_ratingtext = (f'How likely are you to share photos with {partner_name} in the future? \n\n Use your left and right arrows to move the arrow to your desired rating.' )
    event.clearEvents('keyboard')
    futuresharing_slider.markerPos = 2.5
    futuresharing_question_text.setText(futuresharing_ratingtext)
    rating_selected = False  # Reset before the future rating rating loop

    while not rating_selected:  # Keep the screen up until space is pressed
            keys = event.getKeys()  # Get key presses
            display_futuresharing_rating_text.setText(round(futuresharing_slider.getMarkerPos(), 1))  # Update display

            if keys:  # Process keys only if pressed
                if 'left' in keys:
                    futuresharing_slider.markerPos = max(slider_min, futuresharing_slider.markerPos - 0.1)
                    display_futuresharing_rating_text.setText(round(futuresharing_slider.getMarkerPos(), 1))
                elif 'right' in keys:
                    futuresharing_slider.markerPos = min(slider_max, futuresharing_slider.markerPos + 0.1)
                    display_futuresharing_rating_text.setText(round(futuresharing_slider.getMarkerPos(), 1))
                elif 'escape' in keys:
                    save_and_quit()
                elif 'space' in keys:
                    rating_selected = True  # Exit the loop

            # Draw all components before flipping
            futuresharing_slider.draw()
            futuresharing_question_text.draw()
            display_futuresharing_rating_text.draw()
            futuresharing_continue_text.draw()
            partner_avatar_stim.draw()
            win.flip()  # Refresh the screen after updating everything

    # ✅ Return the selected rating  
    return round(futuresharing_slider.getMarkerPos(), 1)

fixation = visual.TextStim(win, text='+', height=0.1, color='white')

def play_sync_tone():
    if os.path.exists('beep.wav'):
        win.flip()  # clears previous content
        fixation.draw()
        beep = sound.Sound('beep.wav')
        beep.play()
        core.wait(3)  # Wait to ensure it finishes
    else:
        print("WARNING: beep.wav not found.")

# Define a list to store trial data
trials_per_block = 30  # Each block has 30 trials
experiment_data = []

# Define the output directory for data storage
data_dir = os.path.join(expdir, "data")

# Ensure the data directory exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Define the output file path
#output_file = os.path.join(data_dir, f"{sub_id}_data.csv")

def save_data():
    """ Save the collected experiment data to CSV. """
    if experiment_data:  
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M.%S")
        filename = f"{sub_id}_RejTask_{timestamp}.csv"
        output_path = os.path.join(data_dir, filename)

        try:
            df_output = pd.DataFrame(experiment_data)
            df_output.to_csv(output_path, index=False)
            print(f"Experiment data saved to: {output_path}")
            print(df_output.head())  # Optional: Preview the first few rows
        except Exception as e:
            print(f"ERROR saving data: {e}")
photo_trial_num = 1
gamble_trial_num = 1

# --- Welcome Screen Instructions ---

welcome_text = """
Welcome to the Social Media Task

In this task, you will have the opportunity to share some of your Instagram photos with other participants and receive feedback. You will also make a series of decisions that could earn you an additional monetary bonus.

You will begin the task with an endowment of $10. At various points, you will choose between two options:

A gamble option, where you have a 50/50 chance of winning a set amount or earning nothing.

A certain option, where you are guaranteed a specific dollar amount.

Each choice will be displayed on the screen for 2 seconds. The gamble option will always appear on the left side of the screen and can be selected by pressing ‘1’. The certain option will always appear on the right side and can be selected by pressing ‘9’.

To begin, you will be randomly assigned a partner by the computer. Your Instagram photos will be shared with this partner, who will indicate whether they like or dislike each one. You will go through this process with four different partners over the course of the task.

Press space to continue.
"""

welcome_stim = visual.TextStim(win=win, text=welcome_text, height=0.8, wrapWidth=30, color='white', pos=(0, 0))
welcome_stim.draw()
win.flip()
event.clearEvents()
event.waitKeys(keyList=['space'])  # Wait for space to proceed

# Example usage:
play_sync_tone()

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

        for first_half_cycle in range(3):  
            photo_batch_start = first_half_cycle * 5
            gamble_batch_start = choice_index  # Track where we are in gamble trials

            # **Show 5 Photo Shares**
            batch_photos = block.iloc[photo_batch_start:photo_batch_start + 5]
            for _, photo_row in batch_photos.iterrows():
                trial = photo_row['TrialNumber']
                print(f"DEBUG: Photo Share Trial {photo_trial_num}")
                response_time_photo = photo_share_screen(win, photo_row)

                experiment_data.append({
                    "SubjectID": sub_id,
                    "PhotoTrialNumber": photo_trial_num,
                    "GambleTrialNumber": None,
                    "Task": "PhotoShare",
                    "Partner": photo_row.get("Partner", ""),
                    "Condition": photo_row.get("Condition", ""),
                    "PhotoFilename": photo_row.get("Photos", ""),
                    "Feedback": photo_row.get("Feedback", ""),
                    "FeedbackWait": photo_row.get("FeedbackWait", None),
                    "PhotoResponseTime": response_time_photo,
                })

                photo_trial_num += 1

            fixation = visual.TextStim(win, text='+', height=1.0, color='white')
            fixation.draw()
            win.flip()
            core.wait(7.0)

            # **Show 5 Gambles**

            batch_gambles = df_gambles.iloc[gamble_batch_start:gamble_batch_start + 5]
            for _, gamble_row in batch_gambles.iterrows():
                print(f"DEBUG: Gamble Trial {gamble_trial_num}")
                response_time_gamble, gamble_choice = gamble_screen(win, gamble_row)

                #determine outcome
                if gamble_choice == 1:
                    selected_price = gamble_row["risky_gain"]
                    gamble_key = '1'
                elif gamble_choice == 0:
                    selected_price = gamble_row["certain"]
                    gamble_key = '9'
                else:
                    selected_price = 999
                    gamble_key = '999'


                experiment_data.append({
                    "SubjectID": sub_id,
                    "PhotoTrialNumber": None,
                    "GambleTrialNumber": gamble_trial_num,
                    "Task": "Gamble",
                    "RiskyGain": gamble_row["risky_gain"],
                    "CertainAmount": gamble_row["certain"],
                    "Outcome":gamble_row["outcome"],
                    "ev_level": gamble_row['ev_level'],
                    "GambleResponseTime": response_time_gamble,
                    "GambleChoice": gamble_choice,
                    "SelectedPrice": selected_price,
                    "GambleKey": gamble_key
                })

                gamble_trial_num += 1

            fixation = visual.TextStim(win, text='+', height=1.0, color='white')
            fixation.draw()
            win.flip()
            core.wait(7.0)


            choice_index += 5  # Move to the next set of gambles

        # ✅ **Midway Emotion Rating After 15 Trials**
        if first_half_cycle == 2:
            print("DEBUG: Mid-block Emotion Rating (after 3 cycles)")
            emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
            experiment_data.append({
                "SubjectID": sub_id,
                "TrialNumber": f"MidEmotion_Block{int(first_trial/30)+1}",
                **emotion_ratings
            })

        for second_half_cycle in range(3, 6):  # cycles 3, 4, 5
            photo_batch_start = (second_half_cycle * 5)  # 15, 20, 25
            batch_photos = block.iloc[photo_batch_start:photo_batch_start + 5]
            batch_gambles = df_gambles.iloc[choice_index:choice_index + 5]

    # -- 5 Photo Trials --
            for _, photo_row in batch_photos.iterrows():
                print(f"DEBUG: Photo Share Trial {photo_trial_num}")
                response_time_photo = photo_share_screen(win, photo_row)
                experiment_data.append({
                    "SubjectID": sub_id,
                    "PhotoTrialNumber": photo_trial_num,
                    "GambleTrialNumber": None,
                    "Task": "PhotoShare",
                    "Partner": photo_row.get("Partner", ""),
                    "Condition": photo_row.get("Condition", ""),
                    "PhotoFilename": photo_row.get("Photos", ""),
                    "Feedback": photo_row.get("Feedback", ""),
                    "FeedbackWait": photo_row.get("FeedbackWait", None),
                    "PhotoResponseTime": response_time_photo,
                })
                photo_trial_num += 1

            fixation = visual.TextStim(win, text='+', height=1.0, color='white')
            fixation.draw()
            win.flip()
            core.wait(7.0)

            # -- 5 Gamble Trials --
            for _, gamble_row in batch_gambles.iterrows():
                print(f"DEBUG: Gamble Trial {gamble_trial_num}")
                response_time_gamble, gamble_choice = gamble_screen(win, gamble_row)

                if gamble_choice == 1:
                    selected_price = gamble_row["risky_gain"]
                    gamble_key = '1'
                elif gamble_choice == 0:
                    selected_price = gamble_row["certain"]
                    gamble_key = '9'
                else:
                    selected_price = 999
                    gamble_key = '999'

                experiment_data.append({
                    "SubjectID": sub_id,
                    "PhotoTrialNumber": None,
                    "GambleTrialNumber": gamble_trial_num,
                    "Task": "Gamble",
                    "RiskyGain": gamble_row["risky_gain"],
                    "CertainAmount": gamble_row["certain"],
                    "Outcome":gamble_row["outcome"],
                    "ev_level": gamble_row['ev_level'],
                    "GambleResponseTime": response_time_gamble,
                    "GambleChoice": gamble_choice,
                    "SelectedPrice": selected_price,
                    "GambleKey": gamble_key
                })
                gamble_trial_num += 1

            fixation = visual.TextStim(win, text='+', height=1.0, color='white')
            fixation.draw()
            win.flip()
            core.wait(7.0)

            choice_index += 5

        # ✅ **Final Emotion + futuresharing Ratings**
        last_trial = block.iloc[-1]['TrialNumber']
        if last_trial in [30, 60, 90, 120]:
            print(f"DEBUG: Final Emotion & futuresharing Ratings on Trial {last_trial}")
            emotion_ratings = display_emotion_ratings(win, emotions, slider_min=0, slider_max=5)
            partner_name = block.iloc[-1]['Partner']  # Get the partner name here
              # Define emoji image paths
            futuresharing_avatar_image.setImage(emoji_paths[partner_name])
            futuresharing_rating_value = futuresharing_rating(win, futuresharing_avatar_image, partner_name)
            experiment_data.append({
                "SubjectID": sub_id,
                "TrialNumber": last_trial,
                **emotion_ratings,
                "futuresharingRating": futuresharing_rating_value
            })

except KeyboardInterrupt:
    print("Experiment interrupted. Saving data...")
    save_data()

except Exception as e:
    print(f"ERROR: {e}\nSaving collected data before exiting.")
    save_data()
    sys.exit(1)

# **Final Save Before Exit**
save_data()

# Redirect to post-task survey
qualtrics_base_url = 'https://adelphiderner.qualtrics.com/jfe/form/SV_cLJA7Y0xl7ry14a'
qualtrics_url = f"{qualtrics_base_url}?sub_id={sub_id}"
core.wait(1.0)
webbrowser.open(qualtrics_url)

# Close PsychoPy window
win.close()
core.quit()









