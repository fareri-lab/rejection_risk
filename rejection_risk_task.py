# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 2025

@author: Jordan Dejoie
"""

#### SLA_imaging ####

# Jordan Dejoie
# 1/2025


### specs ###
# add task description here

### timing ###
# add timing info here

#import modules

from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random
import pandas as pd
from decimal import Decimal

#maindir = os.getcwd()

#parameters
DEBUG = False

frame_rate=1
initial_fixation_dur = 4
final_fixation_dur = 10
instruct_dur=3
outcome_dur=1
trial_dur = 4
decision_dur=2

responseKeys=('1','6','z')
showreturnscreen = 1
#get subjID
if DEBUG:
   subj_id='test' #change with specific test number/as needed
   #friend_id='your friend'
   #other_id='a stranger'
   #version='1'
   #version = int(version)
   session = 'new'
   screen='n'

else:
   startDlg=gui.Dlg(title="SLA")
   startDlg.addField('Session:', choices=["new", "returning"]) #0
   # session=startDlg.data[0] #changed returning var to session
   startDlg.show()
   session=startDlg.data[0]

   # if gui.OK:  # or if ok_data is not None
   if session == 'returning':
       restart = 1
       returnDlg=gui.Dlg(title="REDO: SLA Task")
       returnDlg.addField('Participant: ') #0
       #returnDlg.addField('Enter Friend Name: ') #1
       #returnDlg.addField('Enter Partner Name: ') #NOTE: PARTNER IS THE CONFEDERATE/STRANGER #2
       #returnDlg.addField('Version:',choices=['1', '2']) #3 -- Order
       returnDlg.addField('Condition:',choices=['0', '1', '2']) #4 --  Partners
       returnDlg.addField('Block:', choices=['1', '2', '3']) #5 -- Block within each condition
       returnDlg.addField('Full Screen? (Enter lowercase: y or n):') #6
       returnDlg.show()

       subj_id=returnDlg.data[0]
       #friend_id=returnDlg.data[1]
       #other_id=returnDlg.data[2]
       #version = returnDlg.data[3]
       condition = returnDlg.data[4]
       block= returnDlg.data[5]
       screen=returnDlg.data[6]

   elif session == 'new':
       subjDlg=gui.Dlg(title="SLA")
       subjDlg.addField('Participant: ') #0
       #subjDlg.addField('Enter Friend Name: ') #1
       #subjDlg.addField('Enter Partner Name: ') #NOTE: PARTNER IS THE CONFEDERATE/STRANGER #2
       #subjDlg.addField('Version:',choices=['1', '2']) #3
       subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #4
       subjDlg.show()

       subj_id=subjDlg.data[0]
       #friend_id=subjDlg.data[1]
       #other_id=subjDlg.data[2]
       #version=subjDlg.data[3]
       screen=subjDlg.data[4]


run_data = {
   'Participant ID': subj_id,
   'Date': str(datetime.datetime.now()),
   'Description': 'rejection_risk_task'
   }
useFullScreen= ''
#window setup
if screen == 'y':
   useFullScreen=True
   useDualScreen=1
if screen == 'n':
   useFullScreen=False
   useDualScreen=0
if (screen != 'y') and (screen != 'n'):
   print ('Please specify how you want to present this task. Please enter y (yes) or n (no).')

win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen) #set screen to 1 for dual monitor
insertrecipient = ''
#define stimulus
fixation = visual.TextStim(win, text="+", height=2)
#ready_screen = visual.TextStim(win, text="Great job! Please wait for this round of the game to begin. \n\nRemember to keep your head still!", height=1.5)
#waiting = visual.TextStim(win, text="Waiting...", height=1.5)

#want to load in the two csvs here from the participant_image folder
trials = 'pID_trials.csv'
gambles = 'pID_gambles.csv'
emotions = ['Sadness', 'Anger', 'Happiness', 'Surprise', 'Disgust', 'Excitement']
emoji_path = 
partners = ['Sam', 'Charlie', 'Riley', 'Sam']

#decision screen
# shareStim =  visual.TextStim(win, pos=(0,1.5), height=1)

cue = visual.TextStim(win, pos=(0,1.5), height=1, text= '?')
#pictureStim =  visual.ImageStim(win, pos=(0,8.0), size=(6.65,6.65))
top_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(-10,5),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
top_text = visual.TextStim(win, pos=[-10,5], height=1)
bottom_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(-10,-5),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
bottom_text = visual.TextStim(win, pos=[-10, -5], height=1)
certain_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(10,0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
certain_text = visual.TextStim(win, pos=(10,0), height=1)
outcomeMsg = visual.TextStim(win, pos = (0,1), wrapWidth=20, height = 1.2)
#block_msg = visual.TextStim(win, text='Great job! Please wait to proceed.', pos = (0,1), wrapWidth=20, height = 1.2)
block_msg = visual.TextStim(win, text='Please wait for this round of the game to begin. \n\nRemember to keep your head still!', pos = (0,1), wrapWidth=20, height = 1.2)
start_return = visual.TextStim(win, text = '', pos = (0,1), wrapWidth=20, height = 1.2)
# outcome screen
outcome_stim = visual.TextStim(win, text='')

outcome_map = {
   1: 'You chose the gamble and %s %s',
   2: 'You chose the certain amount of %s',
   999: '#'
   }

# condition_screen = {
#     1: ''
#
# }
# instruction screen #
instruct_screen = visual.TextStim(win, text='In this experiment, you are going to be sharing your photos with other participants for feedback. Intermittently, you will make a series of monetary decisions. \n\nYou will have $24 to start with in this experiment.\n\n  You will have the opportunity to add to this amount based on your decisions.', pos = (0,1), wrapWidth=20, height = 1.2)
instruct_screen2 = visual.TextStim(win, text='On all trials of the experiment, you will be deciding between: \n\n(1) a  50% monetary gamble\n\n OR:\n\n(2) an 100% (i.e. guaranteed) monetary option.',pos = (0,1), wrapWidth=20,height=1.2)
#instruct_screen3 = visual.TextStim(win, text = 'On most trials, you will be presented with a choice between a 50% chance of winning or losing money and a 100% chance of gaining nothing ($0). \n\nOn some trials, the choice will be between a 50% chance of gaining money or gaining $0 and a 100% chance of gaining a different monetary amount.\n\n Please indicate on each trial whether you accept the gamble or prefer the guarnteed option.' , pos = (0,1), wrapWidth=25, height = 1.2)
instruct_screen4 = visual.TextStim(win, text='Press 1 to choose the option on the left side of the screen.\n\n Press 9 to choose the option on the right side of the screen.', pos = (0,1),wrapWidth=20, height = 1.2)
#instruct_screen3 = visual.TextStim(win, text='You will be making three sets of choices throughout the course of the experiment, with a different allotment of $24 each time.  \n\n Some of your choices will affect only you, others will affect someone else.\n\n You will press the ‘1’ key to choose the gamble or the ‘2’ key to choose the guaranteed option, given the amounts shown. Press the spacebar to begin', pos = (0,1),wrapWidth=20, height = 1.2)
condition_screen = visual.TextStim(win,pos = (0,1), wrapWidth=20, height = 0.7)


#exit
exit_screen = visual.TextStim(win, text='Thanks for playing! Please wait for instructions from the researcher.', pos = (0,1), wrapWidth=20, height = 1.2)


#logging
expdir = os.getcwd()
subjdir = '%s/Participant_Images/%s' % (expdir, subj_id)
if not os.path.exists(subjdir):
   os.makedirs(subjdir)

base_dir = os.getcwd()  # Gets the current working directory
participant_images_dir = os.path.join(base_dir, "Participant_Images")

   #timing
globalClock = core.Clock()
timer = core.Clock()


# Load trial data
trial_data = pd.read_csv("trials.csv")
gamble_data = pd.read_csv("gambles.csv")

subj_id = 0  # This will be set dynamically from the dialog box
participant_dir = os.path.join(participant_images_dir, subj_id)

# Path to the trials CSV for the participant
trials_csv_path = os.path.join(participant_dir, "trials.csv")

def partner_match_screen(win, partner_name, emoji_path, load_time=5):
    """
    Display a partner match screen with a loading bar, dynamic text, and an emoji.
    
    Args:
        win: PsychoPy window object.
        partner_name (str): The name of the matched partner.
        emoji_path (str): Path to the emoji image to display.
        load_time (float): Time (in seconds) for the loading bar to fill up.
    """
    # Text for "Please wait to be matched with a partner"
    wait_text = visual.TextStim(
        win,
        text="Please wait to be matched with a partner...",
        pos=(0, 0.3),
        height=0.05,
        color="White"
    )
    
    # Loading bar components
    bar_outline = visual.Rect(
        win,
        width=0.6,
        height=0.05,
        lineColor="White",
        pos=(0, 0),
    )
    bar_fill = visual.Rect(
        win,
        width=0.0,  # Start with no width
        height=0.05,
        fillColor="White",
        pos=(-0.3, 0),  # Align the left edge with the outline
        anchor='left'
    )
    
    # Text for "You have matched with [partner]"
    matched_text = visual.TextStim(
        win,
        text=f"You have matched with {partner_name}!",
        pos=(0, 0.3),
        height=0.05,
        color="White"
    )
    
    #put if clause here to link emojis with specific partners 

    # Emoji image
    emoji_stim = visual.ImageStim(
        win,
        image=emoji_path,
        size=(0.2, 0.2),
        pos=(0, 0.0)  # Positioned below the matched text
    )
    
    # "Press any key to continue" text
    continue_text = visual.TextStim(
        win,
        text="Press any key to continue.",
        pos=(0, -0.3),  # Positioned at the bottom of the screen
        height=0.05,
        color="White"
    )
    
    # Phase 1: Display loading bar filling
    start_time = core.getTime()
    while core.getTime() - start_time < load_time:
        # Calculate progress (0 to 1)
        progress = (core.getTime() - start_time) / load_time
        bar_fill.width = progress * 0.6  # Scale the width to the bar outline
        
        # Draw components
        wait_text.draw()
        bar_outline.draw()
        bar_fill.draw()
        win.flip()
    
    # Phase 2: Display the matched partner text, emoji, and "Press any key to continue"
    matched_text.draw()
    emoji_stim.draw()
    continue_text.draw()
    win.flip()
    
    # Wait for a key press to continue
    event.waitKeys()

#read in stimuli + logging
def photo_share_screen(win, photo_path,feedback_wait):
    # Create the visual stimulus with the photo
    photo_stim = visual.ImageStim(win, image=photo_path, size=(400, 400))
   
     # Create the photo stimulus
    photo_stim = visual.ImageStim(win, image=photo_path, size=(400, 400))
    
    # Text for "Your photo is now being shared"
    sharing_text = visual.TextStim(win, text="Your photo is now being shared.", pos=(0, -0.5), height=0.05, color="White")

    # Text for "Please wait for feedback"
    waiting_text = visual.TextStim(win, text="Please wait for feedback.", pos=(0, -0.5), height=0.05, color="White")
    
    # Phase 1: Display the photo with "Your photo is now being shared"
    photo_stim.draw()
    sharing_text.draw()
    win.flip()
    core.wait(3)  # Display for 3 seconds
    
    # Phase 2: Display the photo with "Please wait for feedback"
    photo_stim.draw()
    waiting_text.draw()
    win.flip()
    core.wait(feedback_wait)  # Display for the feedback_wait duration

def decision_screen(win):
    top_box = visual.Rect(win, width=200, height=100, pos=(-150, 0), fillColor="gray")
    bottom_box = visual.Rect(win, width=200, height=100, pos=(150, 0), fillColor="gray")
    
    top_text = visual.TextStim(win, text="Option 1", pos=(-150, 0), height=24, color="white")
    bottom_text = visual.TextStim(win, text="Option 2", pos=(150, 0), height=24, color="white")
    
    instruction = visual.TextStim(win, text="Choose an option: Left (1) or Right (2)", pos=(0, -300), height=24)
    
    # Draw stimuli
    top_box.draw()
    bottom_box.draw()
    top_text.draw()
    bottom_text.draw()
    instruction.draw()
    win.flip()
    
    # Wait for response
    keys = event.waitKeys(keyList=["1", "2"])
    return keys[0]  # Return the choice

def emotion_rating_screen(win, emotions):
    """
    Display a screen with sliders for rating multiple emotions.
    
    Args:
        win: PsychoPy window object.
        emotions (list of str): List of emotion labels for the sliders.
    """
    # Create sliders and labels for each emotion
    sliders = []
    labels = []
    start_y = 0.4  # Starting position for the first slider (Y-coordinate)
    spacing = -0.15  # Spacing between sliders
    
    for i, emotion in enumerate(emotions):
        # Create a slider for each emotion
        slider = visual.Slider(
            win=win,
            ticks=(0, 1, 2, 3, 4, 5, 6),  # Range from 0 to 6
            labels=["0", "1", "2", "3", "4", "5", "6"],  # Tick labels
            granularity=1,  # Force discrete values
            pos=(0, start_y + i * spacing),  # Position for each slider
            size=(0.8, 0.05),  # Slider size
            style='rating',  # Slider style
            color='White',
            font='Helvetica'
        )
        sliders.append(slider)
        
        # Create a label for each slider
        label = visual.TextStim(
            win=win,
            text=emotion,
            pos=(-0.6, start_y + i * spacing),  # Position left of the slider
            height=0.05,
            color="White",
            alignText="right"
        )
        labels.append(label)
    
    # Instructions
    instructions = visual.TextStim(
        win=win,
        text="Rate how strongly you feel each emotion (0 = not at all, 6 = very strongly).",
        pos=(0, 0.7),
        height=0.06,
        color="White",
        wrapWidth=1.5
    )
    
    # Draw everything on the screen
    while True:
        instructions.draw()
        for slider, label in zip(sliders, labels):
            slider.draw()
            label.draw()
        win.flip()
        
        # Check if participants are ready to continue (e.g., by pressing 'space')
        keys = event.getKeys()
        if "space" in keys:
            break
    
    # Collect ratings
    ratings = [slider.markerPos for slider in sliders]
    return ratings

# Example usage
win = visual.Window(size=(800, 600), color="black", units="height")
emotions = ["Happy", "Sad", "Angry", "Excited", "Calm", "Fearful"]
ratings = emotion_rating_screen(win, emotions)
print(f"Emotion ratings: {ratings}")

win.close()
core.quit()

def photo_feedback_screen(win, partner_name, feedback_type):
    """
    Display a photo feedback screen with the partner's name and feedback.
    
    Args:
        win: PsychoPy window object.
        partner_name (str): The name of the partner.
        feedback_type (str): The feedback type ('liked' or 'did not like').
    """
    # Base directory for feedback images
    image_dir = "Task_Images"  # Replace with your actual directory
    
    # Determine the image filename based on feedback type
    if feedback_type.lower() == "liked":
        image_filename = "thumbsup.jpg"
    elif feedback_type.lower() == "did not like":
        image_filename = "thumbsdown.jpg"
    else:
        image_filename = None  # Default if feedback type is invalid
    
    # Construct the full path to the image
    if image_filename:
        image_path = os.path.join(image_dir, image_filename)
    else:
        image_path = None
    
    # Feedback prompt
    feedback_prompt = visual.TextStim(
        win,
        text=f"{partner_name} {feedback_type} your photo",
        pos=(0, 150),
        height=24
    )
    
    # Image stimulus
    if image_path and os.path.exists(image_path):
        feedback_image = visual.ImageStim(win, image=image_path, size=(400, 400), pos=(0, -100))
    else:
        feedback_image = None  # Handle missing or invalid feedback gracefully
    
    # Draw stimuli
    feedback_prompt.draw()
    if feedback_image:
        feedback_image.draw()
    win.flip()
    
    # Wait for a key press to continue
    event.waitKeys()


def partner_salience_rating(win, partner_name):
    """
    Display a feedback screen with a single slider asking participants how likely
    they would be to share with the specified partner in the future.
    
    Args:
        win: PsychoPy window object.
        partner_name (str): The name of the partner from the CSV.
    
    Returns:
        float: The rating provided by the participant.
    """
    # Instructions with partner's name
    prompt_text = f"How likely are you to share with {partner_name} in the future? (0 = Not at all, 6 = Very likely)"
    prompt = visual.TextStim(
        win=win,
        text=prompt_text,
        pos=(0, 0.4),  # Positioned near the top
        height=0.05,
        wrapWidth=1.5,
        color="White"
    )
    
    # Slider for the response
    slider = visual.Slider(
        win=win,
        ticks=(0, 1, 2, 3, 4, 5, 6),  # 0 to 6 scale
        labels=["0", "1", "2", "3", "4", "5", "6"],  # Tick labels
        granularity=1,  # Discrete values
        size=(1.0, 0.1),  # Size of the slider
        pos=(0, 0),  # Centered horizontally
        color="White",
        font="Helvetica",
        style="rating"
    )
    
    # Instructions to confirm response
    confirm_text = visual.TextStim(
        win=win,
        text="Use the slider to indicate your response and press SPACE to continue.",
        pos=(0, -0.4),  # Positioned near the bottom
        height=0.04,
        wrapWidth=1.5,
        color="White"
    )
    
    # Display the screen and wait for a response
    while True:
        prompt.draw()
        slider.draw()
        confirm_text.draw()
        win.flip()
        
        # Check for space key to confirm
        keys = event.getKeys()
        if "space" in keys and slider.markerPos is not None:  # Ensure a value is selected
            break
    
    # Return the rating provided by the participant
    return slider.markerPos

for i, trial in trial_data.iterrows():
    partner_name = trial["Partner"]  # Extract partner name
    photo_path = trial["Photos"]    # Extract photo path
    trial_number = trial["TrialNumber"] #Extract trial number
    feedback = trial["Feedback"] #Extrack pos or neg feedback
    feedback_wait = trial["FeedbackWait"] #Extract wait time for feedback



for i, trial in trial_data.iterrows():
    # Photo Share Screen
    photo_share_screen(win, trial["photo_path"])
    
    # Decision-Making Screen
    choice = decision_screen(win)
    print(f"Decision: {choice}")  # Log or save the decision
    
    # Likert Rating Screen
    rating = likert_rating_screen(win)
    print(f"Rating: {rating}")  # Log or save the rating

results = []

for i, trial in trial_data.iterrows():
    # Photo Share Screen
    photo_share_screen(win, trial["photo_path"])
    
    # Decision-Making Screen
    choice = decision_screen(win)
    
    # Likert Rating Screen
    rating = likert_rating_screen(win)
    
    # Append results
    results.append({"photo": trial["photo_path"], "choice": choice, "rating": rating})

# Save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("results.csv", index=False)

win.close()
core.quit()

