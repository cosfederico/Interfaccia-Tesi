
import os
import argparse

parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawTextHelpFormatter,
                    description='''This script automatically downloads data from the Empatica S3 Bucket and
synchronizes it with the recorded sessions.''',
                    epilog=
'''HOW TO SET UP YOUR AWS CREDENTIALS

Download and Install the AWS CLI:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- direct download for Windows:  https://awscli.amazonaws.com/AWSCLIV2.msi

After installation, open any terminal, then run:

> aws configure
> AWS Access Key ID [None]: <YOUR_ACCESS_KEY_ID>
> AWS Secret Access Key [None]: <YOU_SECRET_ACCESS_KEY_ID>
> Default region name [None]: <LEAVE_EMPTY>
> Default output format [None]: <LEAVE_EMPTY>

Re-run the script and it should work just fine.
'''
)

parser.parse_args()

HOME = os.getenv('HOME')
if not HOME:
    HOME = os.getenv('USERPROFILE')
if not HOME:
    HOME = '~'
    
if not os.path.isdir(os.path.join(HOME, '.aws')) or not os.path.isfile(os.path.join(HOME, '.aws', 'credentials')):
    import sys
    print("ERROR: No AWS shared credentials found in your system.")
    print("Please download the AWS CLI and setup your access credentials before running this script.")
    print("Read the README.md or run the following command for instructions on how to do that:")
    print("\n\tpython", os.path.split(sys.argv[0])[1], "-h\n")
    quit()

print("loading resources...")

import pandas as pd

from backend.video.process_video import process_video
from backend.empatica.sync_empatica_data import sync_empatica_data
from backend.empatica.download_empatica_data import download_empatica_data
from backend.empatica.avro_to_csv import convert_empatica_data_to_csv
from backend.empatica.hr import estimate_hr
from backend.empatica.rr import estimate_rr

DATA_FOLDER = 'data'

subjects = os.listdir(DATA_FOLDER)

print("Found subjects:", subjects)

while True:
    ans = input("Start data synchronization? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
                  
        for subject in subjects:
            
            subject_dir = os.path.join(DATA_FOLDER, subject)

            print("\nSynchronizing data for Subject", subject)

            subject_data = pd.read_csv(os.path.join(subject_dir, 'data.csv'), sep=';', encoding="latin1") # per le è/é accentate
            start_ts = subject_data['session_start_timestamp'].iloc[0]
            date = subject_data['date'].iloc[0]

            print("\tDownloading Empatica Data...")
            try:
                avro_file_path = download_empatica_data(start_ts, subject_dir, date=date, participant="TEST")
            except:
                print("\tError - No Empatica data found for subject " + subject + ", skipping")
                open(os.path.join(subject_dir, "NO-DATA-FOUND-FOR-THIS-SUBJECT"), 'a').close()
                continue
            
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
            
        print("\nAll data has been synchronized and is ready for analysis.")
                
        break
    
    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        break