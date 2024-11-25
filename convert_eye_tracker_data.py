from backend.config import load_config
import os
import sys
import subprocess
import pandas as pd

try:
    config = load_config()
except Exception as e:
    print("Impossibile caricare il file di config: ", e)
    quit()

def quit():
    input("Press ENTER to quit...")
    sys.exit()

DATA_FOLDER = config['app']['DATA_FOLDER'] 

if not os.path.exists(DATA_FOLDER):
    print("Data folder not existent. Please provide a valid folder in the config.json or start recording some data with the main app to extract some features.")
    quit()

participants = os.listdir(DATA_FOLDER)
if len(participants) == 0:
    print("No recorded data found. Please record some data with the main app, then run this script to extract all facial features from the videos recorded.")
    quit()

print("Found participants:", participants)

while True:
    print("The following script converts all recorded eye-tracker data (.edf files) in .CSV raw data.")
    ans = input("Start conversion for all participants? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
        
        edf_file_name = "eye.edf"
        asc_file_name = "eye.asc"
        
        for participant in participants:
            
            print("\nConverting eye-tracker data for participant", participant)
            
            participant_dir = os.path.join(DATA_FOLDER, participant)
            edf_file = os.path.join(participant_dir, edf_file_name)
            asc_file = os.path.join(participant_dir, "eye.asc")
            if not os.path.exists(edf_file):
                print("\tNo eye-tracker data found for the participant:", participant,"- skipping")
                continue
            
            print("\tSynchronizing data...")
            if os.path.exists(asc_file):
                os.remove(asc_file)
            subprocess.run(["edf2asc", "-neye", edf_file], capture_output=True)
            start_ts = None
            with open(os.path.join(participant_dir, 'eye.asc'), 'r') as f:
                for line in f.readlines():
                    if "START_TS" in line:
                        start_ts = int(line.split('\t')[2])
            os.remove(asc_file)

            if start_ts is None:
                print("\tCould not figure start of eye-tracker recording - skipping")
                continue
            
            print("\tExtracting gaze data...")
            subprocess.run(["edf2asc", "-s", edf_file], capture_output=True)
            
            print("Converting gaze data to CSV...")
            ts = []
            x = []
            y = []
            pupil=[]
            with open(os.path.join(participant_dir, 'eye.asc'), 'r') as f:
                for line in f.readlines():
                    fields = line.split("  ")
                    ts.append(fields[0].strip())
                    x.append(fields[1].strip())
                    y.append(fields[2].strip())
                    pupil.append(fields[3].strip())
                    
            print("\tSaving results...")
            data = pd.DataFrame({"timestamp":ts,"x":x, "y":y, "pupil":pupil})
            data.to_csv("eye.csv", index=False)
            os.remove(asc_file)
        
        print("\nAll facial features have been successfully extracted.")

        break

    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        quit()