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

if os.path.exists(choicetrials_path):
    print(f"Loading spreadsheet: {choicetrials_path}")
    df_gambles = pd.read_csv(choicetrials_path)  # Load spreadsheet
    print(df_gambles.head())  # Display first few rows for debugging
else:
    print("Error")
    core.quit()
    
#timing setup
globalClock = core.Clock()

#window setup
useFullScreen = (screen == 'y')
win = visual.Window([1920, 1080], monitor="testMonitor", units="deg",fullscr=useFullScreen, allowGUI=True, screen=0)

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

def gamble_screen(win,row):
    # Reset colors each trial
    top_text.setColor('white')
    bottom_text.setColor('white')
    certain_text.setColor('white')
    #probability_text.setColor('white')

    # Extract values from the spreadsheet
    #probability_text.text = str(row['win_probability'])
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
            quit()

        elif resp == '1':  # Risky option selected
            gamble_choice = 1
            top_text.setColor('orange')
           # probability_text.setColor('green')
            bottom_text.setColor('orange')

        elif resp == '9':  # Certain option selected
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


# --- Welcome Screen Instructions ---

welcome_text = """
Welcome to the Social Media Task

In this task, you will have the opportunity to share some of your Instagram photos with other participants and receive feedback. You will also make a series of decisions that could earn you an additional monetary bonus.

You will begin the task with an endowment of $X. At various points, you will choose between two options:

A gamble option, where you have a 50/50 chance of winning a set amount or earning nothing.

A certain option, where you are guaranteed a specific dollar amount.

Each choice will be displayed on the screen for 2 seconds. The gamble option will always appear on the left side of the screen and can be selected by pressing ‘1’. The certain option will always appear on the right side and can be selected by pressing ‘9’.

To begin, you will have an opportunity to practice making choices.

Press space to begin practicing.
"""

welcome_stim = visual.TextStim(win=win, text=welcome_text, height=0.8, wrapWidth=30, color='white', pos=(0, 0))
welcome_stim.draw()
win.flip()
event.clearEvents()
event.waitKeys(keyList=['space'])  # Wait for space to proceed

# Loop through each row in the gamble trials DataFrame
for index, row in df_gambles.iterrows():
    # Display the gamble screen and capture response
    response_time, choice = gamble_screen(win, row)

    # Optional: Print or log the results
    print(f"Trial {index+1}: Response Time = {response_time}, Choice = {choice}")

     # Check if escape was pressed
    keys = event.getKeys()
    if 'escape' in keys:
        print("Escape key pressed. Exiting experiment.")
        win.close()
        core.quit()

    # Inter-trial interval (7 seconds pause)
    win.flip()  # Clear screen
    core.wait(2)
