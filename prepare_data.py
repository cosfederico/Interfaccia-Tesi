import os
import pandas as pd

from backend.video.process_video import *
from backend.empatica.sync_empatica_data import *
from backend.empatica.download_empatica_data import *
from backend.empatica.avro_to_csv import *
from backend.empatica.hr import *
from backend.empatica.rr import *

DATA_FOLDER = 'data'

subjects = os.listdir(DATA_FOLDER)

print("Found subjects:", subjects)

while True:
    ans = input("Start data synchronization? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
                  
        for subject in subjects:
            
            subject_dir = os.path.join(DATA_FOLDER, subject)

            print("Synchronizing data for Subject", subject)

            subject_data = pd.read_csv(os.path.join(subject_dir, 'data.csv'), sep=';')
            start_ts = subject_data['session_start_timestamp'].iloc[0]
            date = subject_data['date'].iloc[0]

            print("\tDownloading Empatica Data...")
            avro_file_path = download_empatica_data(start_ts, subject_dir, date=date, participant="TEST")
            print("\tConverting Empatica Data to csv...")
            convert_empatica_data_to_csv(avro_file_path, delete_avro_after=True)
            print("\tSynchronizing Empatica data with video capture...")
            sync_empatica_data(subject_dir)
            print("\tExtracting Heart Rate (HR)...")
            estimate_hr(subject_dir, save_to_file=True, delete_peaks_file_after=True)
            print("\tExtracting Respiratory Rate (RR)...")
            estimate_rr(subject_dir, save_to_file=True, delete_bvp_file_after=True)
            print("\tExtracting landmarks and REF from video with Libreface...")
            process_video(subject_dir)
            print("\tDone, next subject")
            
        print("All data has been synchronized and is ready for analysis.")
                
        break
    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        break
