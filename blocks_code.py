# Import modules
from psychopy import visual, core, event, gui
import os
import pandas as pd

# Parameters
DEBUG = False
decision_dur = 2  # Choices shown for 2 seconds
frame_rate = 1
initial_fixation_dur = 4
final_fixation_dur = 10
instruct_dur = 3
trial_dur = 5
choiceKeys = ('1', '9', 'z')

# Get subjID
if DEBUG:
    sub_id = 'test'
    session = 'new'
    screen = 'n'
else:
    startDlg = gui.Dlg(title="SM Task")
    startDlg.addField('Session:', choices=["new", "returning"])
    startDlg.show()
    session = startDlg.data[0]

    subjDlg = gui.Dlg(title="SM Task")
    subjDlg.addField('Participant ID:')
    subjDlg.addField('Full Screen? (Enter lowercase: y or n):')
    subjDlg.show()
    sub_id = subjDlg.data[0]
    screen = subjDlg.data[1]

# Initialize paths
expdir = os.getcwd()
subdir = f"{expdir}/Participant_Images/{sub_id}"

if not os.path.exists(subdir):
    print(f"Error: Directory {subdir} does not exist!")
    core.quit()

choicetrials_path = os.path.join(subdir, f"{sub_id}_gambles.csv")
photoshare_path = os.path.join(subdir, f"{sub_id}_trials.csv")

# Load gamble trials
if os.path.exists(choicetrials_path):
    df_gambles = pd.read_csv(choicetrials_path)
else:
    print(f"Error: Spreadsheet {choicetrials_path} not found in {subdir}")
    core.quit()

# Load photo-sharing trials
if os.path.exists(photoshare_path):
    df_photoshare = pd.read_csv(photoshare_path)
else:
    print(f"Error: Spreadsheet {photoshare_path} not found in {subdir}")
    core.quit()

print("Columns in df_photoshare:", df_photoshare.columns)
print("Columns in df_gambles:", df_gambles.columns)


# Timing setup
globalClock = core.Clock()

# Window setup
useFullScreen = (screen == 'y')
win = visual.Window([800, 600], monitor="testMonitor", units="deg",fullscr=useFullScreen, allowGUI=True, screen=0)

# Define stimuli for gamble screens
top_box = visual.Rect(win, width=9.0, height=7.0, pos=(-10, 5),lineWidth=5, lineColor='white', fillColor='black')
top_text = visual.TextStim(win, text="", pos=[-10, 5], height=1)
probability_text = visual.TextStim(win, text='', pos=[-10, 10.5], height=1)
bottom_box = visual.Rect(win, width=9.0, height=7.0, pos=(-10, -5),lineWidth=5, lineColor='white', fillColor='black')
bottom_text = visual.TextStim(win, text="$0", pos=[-10, -5], height=1)
certain_box = visual.Rect(win, width=9.0, height=7.0, pos=(10, 0),lineWidth=5, lineColor='white', fillColor='black')
certain_text = visual.TextStim(win, text="", pos=(10, 0), height=1)
cue = visual.TextStim(win, text="Make your choice", pos=(0, 10.5), height=1)

# Define stimuli for photo share screen
photoshare_text = visual.TextStim(win, text="Your photo is now being shared.", pos=(0, 11), height=1)

# Define trial ranges
trial_ranges = [(1, 30), (31, 60), (61, 90), (91, 120)]

# Loop through each trial range
for start_trial, end_trial in trial_ranges:

    # Filter trials for the current range
    df_photoshare_filtered = df_photoshare[
        (df_photoshare['TrialNumber'] >= start_trial) & (df_photoshare['TrialNumber'] <= end_trial)]
    df_gambles_filtered = df_gambles[
        (df_gambles['ChoiceNumber'] >= start_trial) & (df_gambles['ChoiceNumber'] <= end_trial)]

print(f"Photo trials in range {start_trial}-{end_trial}:")
print(df_photoshare_filtered)

print(f"Gamble trials in range {start_trial}-{end_trial}:")
print(df_gambles_filtered)



print("Filtered Photo Trials (first 5 rows):")
print(df_photoshare_filtered.head())  # Show filtered photo trials

if df_photoshare_filtered.empty:
    print("WARNING: No photo trials found in the selected range!")


    # Split into chunks of 5 trials
    photo_chunks = [df_photoshare_filtered.iloc[i:i+5] for i in range(0, len(df_photoshare_filtered), 5)]
    gamble_chunks = [df_gambles_filtered.iloc[i:i+5] for i in range(0, len(df_gambles_filtered), 5)]

    # Loop through 5-trial blocks
    for photo_chunk, gamble_chunk in zip(photo_chunks, gamble_chunks):

        ####### STEP 1: DISPLAY 5 PHOTO TRIALS #######
        print("Starting photo trials...")
        for index, row in photo_chunk.iterrows():
            print(f"Photo trial {index}: {row['Photos']}")
            photo_file = row['Photos']
            full_photo_path = os.path.join(expdir, photo_file)  # Use expdir for correct base directory

            if not os.path.exists(full_photo_path):
                print(f"Error: Photo {full_photo_path} not found! Skipping trial {index}.")
                continue

            photo_displayed = visual.ImageStim(win, image=full_photo_path, size=(10, 10), pos=(0, 0))
            photoshare_text.draw()
            photo_displayed.draw()
            win.flip()
            core.wait(2)  # Show for 2 seconds

        ####### STEP 2: DISPLAY 5 GAMBLE TRIALS #######
        print("Starting gamble trials...")
        for index, row in gamble_chunk.iterrows():
            print(f"Gamble trial {index}: Risky Gain={row['risky_gain']}, Certain={row['certain']}")
            # Reset colors
            top_text.setColor('white')
            bottom_text.setColor('white')
            certain_text.setColor('white')
            probability_text.setColor('white')

            # Extract values
            probability_text.text = str(row['win_probability'])
            top_text.text = str(row['risky_gain'])
            certain_text.text = str(row['certain'])

            # Display choices
            top_box.draw()
            top_text.draw()
            bottom_box.draw()
            bottom_text.draw()
            certain_box.draw()
            certain_text.draw()
            probability_text.draw()
            win.flip()
            core.wait(2)

            # Show "Make Your Choice" and Wait for Response
            cue.draw()
            top_box.draw()
            top_text.draw()
            bottom_box.draw()
            bottom_text.draw()
            certain_box.draw()
            certain_text.draw()
            probability_text.draw()
            win.flip()

            event.clearEvents()
            resp = None
            response_timer = core.Clock()

            while response_timer.getTime() < decision_dur:
                resp = event.getKeys(keyList=choiceKeys)
                if resp:
                    resp = resp[0]
                    break

            # Process response
            if resp:
                if resp == 'z':  # Quit
                    win.close()
                    core.quit()
                elif resp == '1':  # Risky option
                    top_text.setColor('green')
                    probability_text.setColor('green')
                    bottom_text.setColor('green')
                elif resp == '9':  # Certain option
                    certain_text.setColor('green')
            else:
                top_text.setColor('red')
                bottom_text.setColor('red')
                certain_text.setColor('red')

            # Display feedback
            top_box.draw()
            top_text.draw()
            bottom_box.draw()
            bottom_text.draw()
            certain_box.draw()
            certain_text.draw()
            probability_text.draw()
            cue.draw()
            win.flip()
            core.wait(1)

# Close experiment
win.close()
core.quit()
