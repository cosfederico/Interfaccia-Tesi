import boto3
import os
import numpy as np

import avro.schema
import avro.datafile
import avro.io

def concat_avro_files(input_files, output_file, delete_original_files=False):
    
    with open(input_files[0], "rb") as f:
        reader = avro.datafile.DataFileReader(f, avro.io.DatumReader())
        schema_json = reader.meta.get("avro.schema").decode("utf-8")
        schema = avro.schema.parse(schema_json)
    
    with open(output_file, "wb") as out_f:
        writer = avro.datafile.DataFileWriter(out_f, avro.io.DatumWriter(), schema)
        
        for file in input_files:
            with open(file, "rb") as f:
                reader = avro.datafile.DataFileReader(f, avro.io.DatumReader())

                file_schema_json = reader.meta.get("avro.schema").decode("utf-8")
                if file_schema_json != schema_json:
                    raise ValueError(f"Schema mismatch in file: {file}")

                for record in reader:
                    writer.append(record)

                reader.close()

        writer.close()

        if delete_original_files:
            for file in input_files:
                try:
                    os.remove(file)
                except:
                    pass

        return output_file

def download_empatica_data(start_ts, end_ts, subject_dir, date, participant, bucket_name, prefix, org_id, study_id):
    
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    
    filter = prefix + org_id + "/" + study_id + "/participant_data/"+ date + "/" + participant

    bucket_objects = bucket.objects.filter(Prefix = filter)
    if len(list(bucket_objects)) == 0:
        raise ValueError("No data found for the selected date: " + date + " and participant: " + participant)

    timestamps = []
    keys = []
    keys_after = []

    for my_bucket_object in bucket_objects:
        
        key = my_bucket_object.key
        
        if not key.endswith(".avro"):
            continue
        
        _, filename = os.path.split(key)
        avro_ts = int(filename[4+len(participant)+1:-5]) 
        
        if avro_ts <= start_ts:
            timestamps.append(avro_ts)
            keys.append(key)

        if avro_ts > start_ts and avro_ts <= end_ts:
            keys_after.append(key)
        
    if len(timestamps) == 0:
        raise ValueError("No recorded data found for the time of this session")
  
    start_files = np.rec.fromarrays((timestamps, keys), names=('ts', 'keys'))    
    file_to_download = start_files.keys[np.argmax(start_files.ts)]

    files_to_download = [file_to_download]
    for key_after in keys_after:
        files_to_download.append(key_after)

    downloaded_files = []
    for file_to_download in files_to_download:
        filename = os.path.split(file_to_download)[1]
        downloaded_file = os.path.join(subject_dir, filename)
        bucket.download_file(file_to_download, downloaded_file)
        downloaded_files.append(downloaded_file)

    if len(downloaded_files) == 1:
        return downloaded_files[0]
    else:
        return concat_avro_files(downloaded_files, os.path.join(subject_dir, "empatica.avro"), delete_original_files=True)