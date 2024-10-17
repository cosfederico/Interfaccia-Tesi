import boto3
import os
import numpy as np

BUCKET_NAME = "empatica-us-east-1-prod-data"
PREFIX = "v2/716/"

def download_empatica_data(start_ts, subject_dir, date, participant):
    
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(BUCKET_NAME)
    
    filter = PREFIX + "1/1/participant_data/"+ date + "/" + participant

    timestamps = []
    keys = []
    
    bucket_objects = bucket.objects.filter(Prefix = filter)
    if len(list(bucket_objects)) == 0:
        raise ValueError("No data found for the selected date: " + date + " and participant: " + participant)

    for my_bucket_object in bucket_objects:
        
        key = my_bucket_object.key
        
        if not key.endswith(".avro"):
            continue
        
        _, filename = os.path.split(key)
        avro_ts = int(filename[4+len(participant)+1:-5]) 
        
        if avro_ts <= start_ts:
            timestamps.append(avro_ts)
            keys.append(key)
      
    if len(timestamps) == 0:
        raise ValueError("No recorded data found for the time of this session")
  
    selected_files = np.rec.fromarrays((timestamps, keys), names=('ts', 'keys'))    
    file_to_download = selected_files.keys[np.argmax(selected_files.ts)]
    filename = os.path.split(file_to_download)[1]

    downloaded_file = os.path.join(subject_dir, filename)

    bucket.download_file(file_to_download, downloaded_file)
    
    return downloaded_file