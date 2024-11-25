print("loading resources...")

from backend.config import load_config
import os

config = load_config()
print("successfully loaded config")

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
    print("The following script extracts all facial features (AU, landmarks, REF, ..) from the recorded sessions using the module Py-feat.")
    ans = input("Start facial feature extraction for all participants? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
        from backend.video.process_video import process_video
                  
        for participant in participants:
            
            participant_dir = os.path.join(DATA_FOLDER, participant)
            print("\Extracting AU, landmarks and REF for participant", participant, "...")
            process_video(participant_dir)
            
        print("\nAll facial features have been successfully extracted.")

        break

    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        break