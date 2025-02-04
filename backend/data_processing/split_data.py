from backend.config import load_config
import os
import shutil
import subprocess
import pandas as pd

def split_gaze_data(dest_dir):
    eye = pd.read_csv(os.path.join(participant_dir, 'eye.csv'))
    eye[(eye["timestamp"] >= video0_start) & (eye["timestamp"] <= video0_end)].to_csv(os.path.join(dest_dir, "eye_" + video0_type.lower() + ".csv"), index=False)
    eye[(eye["timestamp"] >= video1_start) & (eye["timestamp"] <= video1_end)].to_csv(os.path.join(dest_dir, "eye_" + video1_type.lower() + ".csv"), index=False)

    for file in ['fixations', 'saccades']:
        df = pd.read_csv(os.path.join(participant_dir, file + ".csv"))

        df[((df["start_time"] >= video0_start) & (df["start_time"] <= video0_end)) 
            | ((df["end_time"] >= video0_start) & (df["end_time"] <= video0_end))].to_csv(os.path.join(dest_dir, file + "_" + video0_type.lower() + ".csv"), index=False)
        df[((df["start_time"] >= video1_start) & (df["start_time"] <= video1_end)) 
            | ((df["end_time"] >= video1_start) & (df["end_time"] <= video1_end))].to_csv(os.path.join(dest_dir, file + "_" + video1_type.lower() + ".csv"), index=False)


def split_empatica_data(dest_dir):
    for file in ['hr', 'eda', 'bvp']:
        df = pd.read_csv(os.path.join(participant_dir, file + ".csv"))
        df[(df["unix_timestamp"] >= video0_start * 1e6) & (df["unix_timestamp"] <= video0_end * 1e6)].to_csv(os.path.join(dest_dir, file + "_" + video0_type.lower() + ".csv"), index=False)
        df[(df["unix_timestamp"] >= video1_start * 1e6) & (df["unix_timestamp"] <= video1_end * 1e6)].to_csv(os.path.join(dest_dir, file + "_" + video1_type.lower() + ".csv"), index=False)

def split_videos(dest_dir):

    for file in ["webcam", "screen"]:

        video_path = os.path.join(participant_dir, file + ".mp4")
        
        ffmpeg0 = [
            'ffmpeg',
            '-y',
            '-ss', str(video0_start - session_start),
            '-t' , str(video0_end - video0_start),
            '-i', video_path,
            '-codec', 'copy',
            os.path.join(dest_dir, file + "_" + video0_type.lower() + ".mp4")
        ]

        ffmpeg1 = [
            'ffmpeg',
            '-y',
            '-ss', str(video1_start - session_start),
            '-t' , str(video1_end - video1_start),
            '-i', video_path,
            '-codec', 'copy',
            os.path.join(dest_dir, file + "_" + video1_type.lower() + ".mp4")
        ]

    subprocess.run(ffmpeg0, capture_output=True)
    subprocess.run(ffmpeg1, capture_output=True)

def copy_remaining_files(dest_dir):
    for file in ['fs.json']:
        shutil.copy(os.path.join(participant_dir, file), dest_dir)

try:
    config = load_config()
except Exception as e:
    print("Impossibile caricare il file di config: ", e)
    quit()

DATA_FOLDER = config['app']['DATA_FOLDER'] 

if not os.path.exists(DATA_FOLDER):
    print("Data folder not existent. Please provide a valid folder in the config.json or start recording some data with the main app to extract some features.")
    quit()

participants = os.listdir(DATA_FOLDER)
if len(participants) == 0:
    print("No recorded data found. Please record some data with the main app, then run this script to extract all facial features from the videos recorded.")
    quit()

print("Found participants:", participants)

print("This script takes all recorded data and splits into groups for real and fake videos. Run this for all found participants?")
while True:
    ans = input("Start conversion for all participants? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")

        for participant in participants:

            print("\nSplitting data for participant", participant)
            participant_dir = os.path.join(DATA_FOLDER, participant)
            data = pd.read_csv(os.path.join(participant_dir, 'data.csv'), sep=';', encoding='latin')

            session_start = data["Session Start Timestamp"][0]

            video0_start = data["Video Start Timestamp"][0]
            video0_end = data["Video End Timestamp"][0]
            video0_type = data["Video Type"][0]

            video1_start = data["Video Start Timestamp1"][0]
            video1_end = data["Video End Timestamp1"][0]
            video1_type = data["Video Type1"][0]

            split_dir = "split_data"
            dest_dir = os.path.join(split_dir, participant)
            os.makedirs(dest_dir, exist_ok=True)

            print("\tSplitting gaze data...")
            split_gaze_data(dest_dir=dest_dir)

            print("\tSplitting Empatica data...")
            split_empatica_data(dest_dir=dest_dir)

            print("\tSplitting videos...")
            split_videos(dest_dir=dest_dir)

            print("\tCopying remaining files...")
            copy_remaining_files(dest_dir=dest_dir)

        print("\nAll data has been split and saved in the directory: " + split_dir + ".")
        break

    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        break