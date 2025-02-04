from backend.config import load_config
import os
import sys
import subprocess
import pandas as pd
import numpy as np

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

print("The following script extracts from all recorded eye-tracker data (.edf files) fixations and saccades events (.csv).")
while True:
    ans = input("Start conversion for all participants? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
        
        edf_file_name = "eye.edf"
        asc_file_name = "eye.asc"
        
        for participant in participants:
            
            print("\nConverting eye-tracker data for participant", participant)
            
            participant_dir = os.path.join(DATA_FOLDER, participant)

            files_in_dir = os.listdir(participant_dir)
            if 'fixations.csv' in files_in_dir and 'saccades.csv' in files_in_dir and 'blinks.csv' in files_in_dir:
                print("\tGaze features already extracted for this participant - skipping")
                continue

            edf_file = os.path.join(participant_dir, edf_file_name)
            asc_file = os.path.join(participant_dir, "eye.asc")
            if not os.path.exists(edf_file):
                print("\tNo eye-tracker data found for the participant: ", participant," - skipping")
                continue
            
            print("\tSynchronizing data...")
            if os.path.exists(asc_file):
                os.remove(asc_file)
            
            data = pd.read_csv(os.path.join(participant_dir, 'data.csv'), sep=';', encoding='latin')
            try:
                tracker_start_relative_ts = data["EyeTracker_Start_Tracker_Time"][0]
                tracker_start_absolute_ts = data["EyeTracker_Start_Tracker_Time_TS"][0]
            except:
                print("\tNo eye-tracker synchronization data found for the participant: ", participant, " - skipping")
            
            print("\tExtracting events data...")
            subprocess.run(["edf2asc", "-y", "-nst", "-nmsg","-t", "-e", edf_file], capture_output=True)
            
            print("\tConverting events data to CSV...")
            fixations = []
            saccades = []
            blinks = []

            with open(os.path.join(participant_dir, 'eye.asc'), 'r') as f:
                for line in f.readlines():
                    if not line.startswith("EFIX") and not line.startswith("ESACC") and not line.startswith("EBLINK"):
                        continue 
                    line = line.strip()
                    fields = [field.strip() for field in line.split("\t")]
                    fields[2] = (int(fields[2]) - tracker_start_relative_ts) / 1e3 + tracker_start_absolute_ts
                    fields[3] = (int(fields[3]) - tracker_start_relative_ts) / 1e3 + tracker_start_absolute_ts
                    fields[4] = int(fields[4]) / 1e3
                    event = fields[0]
                    if event == "EFIX":
                        fixations.append(fields)
                    elif event == "ESACC":
                        saccades.append(fields)
                    elif event == "EBLINK":
                        blinks.append(fields)

            fixations = np.array(fixations)
            saccades = np.array(saccades)
            blinks = np.array(blinks)

            print("\tSaving results...")
            pd.DataFrame({
                "eye":fixations[:,1],
                "start_time":fixations[:,2],
                "end_time":fixations[:,3],
                "duration":fixations[:,4],
                "avg_x":fixations[:,5],
                "avg_y":fixations[:,6],
                "avg_pupil":fixations[:,7]
            }).to_csv(os.path.join(participant_dir, "fixations.csv"), index=False)

            pd.DataFrame({
                "eye":saccades[:,1],
                "start_time":saccades[:,2],
                "end_time":saccades[:,3],
                "duration":saccades[:,4],
                "start_x":saccades[:,5],
                "start_y":saccades[:,6],
                "end_x":saccades[:,7],
                "end_y":saccades[:,8],
                "amp":saccades[:,9],
                "peak_vel":saccades[:,10]
            }).to_csv(os.path.join(participant_dir, "saccades.csv"), index=False)
            
            pd.DataFrame({
                "eye":blinks[:,1],
                "start_time":blinks[:,2],
                "end_time":blinks[:,3],
                "duration":blinks[:,4]
            }).to_csv(os.path.join(participant_dir, "blinks.csv"), index=False)

            os.remove(asc_file)
        
        print("\nAll eye-tracking data has been converted and synchronized.")
        break

    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        break