#import modules

from psychopy import visual, core, event, gui, data, sound, logging
import os
import sys
import csv
import datetime
import random
import pandas as pd
from decimal import Decimal

#parameters
DEBUG = False

frame_rate=1
initial_fixation_dur = 4
final_fixation_dur = 10
instruct_dur=3
decision_dur=1
trial_dur=5

choiceKeys=('1','9','z')
showreturnscreen = 1

#get subjID
if DEBUG:
   sub_id='test' #change with specific test number/as needed
   session = 'new'
   screen='n'

else:
   startDlg=gui.Dlg(title="SM Task")
   startDlg.addField('Session:', choices=["new", "returning"]) #0
   # session=startDlg.data[0] #changed returning var to session
   startDlg.show()
   session=startDlg.data[0]

# if gui.OK:  # or if ok_data is not None
   if session == 'returning':
       restart = 1
       returnDlg=gui.Dlg(title="REDO: SM Task")
       returnDlg.addField('Participant ID: ') #0
       returnDlg.addField('Full Screen? (Enter lowercase: y or n):') #6
       returnDlg.show()

       sub_id=returnDlg.data[0]
       screen=returnDlg.data[1]

   elif session == 'new':
       subjDlg=gui.Dlg(title="SM Task")
       subjDlg.addField('Participant ID: ') #0
       subjDlg.addField('Full Screen? (Enter lowercase: y or n):') #4
       subjDlg.show()

       sub_id=subjDlg.data[0]
       screen=subjDlg.data[1]

#initialize path to main experiment directory and subject directory 
expdir = os.getcwd()
subdir = '%s/Participant_Images/%s' % (expdir, sub_id)

#timing
globalClock = core.Clock()
timer = core.Clock()

test_spreadsheets = sub_id

run_data = {
   'Participant ID': sub_id,
   'Date': str(datetime.datetime.now()),
   'Description': 'SM Task'
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


#win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=useFullScreen, allowGUI=False, screen=useDualScreen) #set screen to 1 for dual monitor
win = visual.Window([800, 600], monitor="testMonitor", units="deg",fullscr=True, allowGUI=True, screen=0)

#pictureStim =  visual.ImageStim(win, pos=(0,8.0), size=(6.65,6.65))
top_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(-10,5),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
top_text = visual.TextStim(win, pos=[-10,5], height=1)
bottom_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(-10,-5),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
bottom_text = visual.TextStim(win, pos=[-10, -5], height=1)
certain_box = visual.Rect(win=win, name='polygon', width=(9.0,9.0)[0], height=(7.0,7.0)[1], ori=0, pos=(10,0),lineWidth=5, lineColor=[1,1,1], lineColorSpace='rgb',fillColor=[0,0,0], fillColorSpace='rgb',opacity=1, depth=0.0, interpolate=True)
certain_text = visual.TextStim(win, pos=(10,0), height=1)
#outcomeMsg = visual.TextStim(win, pos = (0,1), wrapWidth=20, height = 1.2)
#block_msg = visual.TextStim(win, text='Great job! Please wait to proceed.', pos = (0,1), wrapWidth=20, height = 1.2)
block_msg = visual.TextStim(win, text='Press any key to continue.', pos = (0,1), wrapWidth=20, height = 1.2)
start_return = visual.TextStim(win, text = '', pos = (0,1), wrapWidth=20, height = 1.2)
# outcome screen

timer.reset()

event.clearEvents()

resp = []

resp_val=None
resp_onset=None

cue = visual.TextStim(win, text="Make your choice", pos=(0, 5), height=1)

#answer=0
trial_onset=globalClock.getTime()

while timer.getTime() < decision_dur:
    # shareStim.draw()
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    win.flip()

    resp != event.waitKeys(keyList = choiceKeys)
    resp = event.waitKeys()
    print(f"Captured response: {resp}")


cue_onset = globalClock.getTime()

while timer.getTime() < trial_dur:
# shareStim.draw()
    cue.draw()
    top_box.draw()
    top_text.draw()
    bottom_box.draw()
    bottom_text.draw()
    certain_box.draw()
    certain_text.draw()
    win.flip()
    stim_duration = cue_onset - trial_onset
    event.clearEvents()
    resp = event.waitKeys(keyList = choiceKeys)
    print(f"Captured response: {resp}")  # Debugging line
    

    if len(resp) > 0:
        if resp[0] == 'z':
            os.chdir(subjdir)
            trials.saveAsWideText(fileName)
            os.chdir(expdir)
            win.close()
            core.quit()
        resp_val = int(resp[0])
    
        if resp_val == 9:
            top_text.setColor('green')
            bottom_text.setColor('green')
    
        elif resp_val == 1:
            certain_text.setColor('green')
        # shareStim.draw()
        top_box.draw()
        top_text.draw()
        bottom_box.draw()
        bottom_text.draw()
        certain_box.draw()
        certain_text.draw()
        cue.draw()
        win.flip()
        resp_onset = globalClock.getTime()
        rt = resp_onset - cue_onset
        core.wait(.1)
        break
else:
    resp_val = 999
    top_text.setColor('red')
    bottom_text.setColor('red')
    certain_text.setColor('red')
    resp_onset = globalClock.getTime()
    rt = resp_onset - cue_onset

    core.wait(.1)


