import os
import sys
import argparse
import json

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

If you still have problems accessing Empatica Data, please refer to their official guide for Data Access:
https://manuals.empatica.com/ehmp/careportal/data_access/v2.7e/en.pdf
'''
)

parser.parse_args()

def quit():
    input("Press ENTER to quit...")
    sys.exit()

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

from backend.config import load_config

try:
    config = load_config()
except Exception as e:
    print("Impossibile caricare il file di config: ", e)
    quit()

DATA_FOLDER = config['app']['DATA_FOLDER'] 
BUCKET_NAME = config['empatica']['BUCKET_NAME']
PREFIX = config['empatica']['PREFIX']
PARTICIPANT_ID = config['empatica']['PARTICIPANT_ID']
ORG_ID = config['empatica']['ORG_ID']
STUDY_ID = config['empatica']['STUDY_ID']

if not os.path.exists(DATA_FOLDER):
    print("Data folder not existent. Please provide a valid folder in the config.json or start recording some data with the main app.")
    quit()

participants = os.listdir(DATA_FOLDER)
if len(participants) == 0:
    print("No recorded data found. Please record some data with the main app, then run this script to download the Empatica data associated with the recordings.")
    quit()

from backend.empatica.sync_empatica_data import sync_empatica_data
from backend.empatica.download_empatica_data import download_empatica_data
from backend.empatica.avro_to_csv import convert_empatica_data_to_csv
from backend.empatica.hr import estimate_hr
from backend.empatica.rr import estimate_rr

print("Found participants:", participants)

while True:
    print("This script automatically downloads physiological data from the Empatica servers and synchronizes it with the recorded sessions.")
    ans = input("Start data download and synchronization for all participants? [yes/no] ").lower()
    
    if ans == 'yes' or ans == 'y':
        print("Starting..")
        import pandas as pd
                  
        for participant in participants:
            
            participant_dir = os.path.join(DATA_FOLDER, participant)

            print("\nSynchronizing data for participant", participant)

            participant_data = pd.read_csv(os.path.join(participant_dir, 'data.csv'), sep=';', encoding="latin1") # per le è/é accentate
            start_ts = participant_data['session_start_timestamp'].iloc[0]
            date = participant_data['date'].iloc[0]

            print("\tDownloading Empatica Data...")
            try:
                avro_file_path = download_empatica_data(start_ts, participant_dir,
                                                        date=date,
                                                        participant=PARTICIPANT_ID,
                                                        bucket_name=BUCKET_NAME,
                                                        prefix=PREFIX,
                                                        org_id=ORG_ID,
                                                        study_id=STUDY_ID)
            except ValueError as e:
                print("\t", e, "- skipping")
                open(os.path.join(participant_dir, "NO-DATA-FOUND-FOR-THIS-PARTICIPANT"), 'a').close()
                continue
            except Exception as e:
                print("\n", e)
                print("Something went wrong while downloading data from Empatica. Are the shared access credentials correct?")
                quit()
            
            print("\tConverting Empatica Data to csv...")
            convert_empatica_data_to_csv(avro_file_path, delete_avro_after=True)
            print("\tSynchronizing Empatica data with video capture...")
            sync_empatica_data(participant_dir)
            print("\tExtracting Heart Rate (HR)...")
            estimate_hr(participant_dir, save_to_file=True, delete_peaks_file_after=True)
            print("\tExtracting Respiratory Rate (RR)...")
            with open(os.path.join(participant_dir, "fs.json"), 'r') as f:
                fs = json.load(f)      
            estimate_rr(participant_dir, fs=int(fs["bvp"]), save_to_file=True, delete_bvp_file_after=False)
            
        print("\nAll available data has been downloaded synchronized and is ready for analysis.")
                
        break
    
    elif ans == 'no' or ans == 'n':
        print("No action taken.")
        quit()