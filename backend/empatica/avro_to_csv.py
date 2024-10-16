from avro.datafile import DataFileReader
from avro.io import DatumReader
import os
import csv

def convert_empatica_data_to_csv(avro_file_path, output_dir=None, delete_avro_after=False):
    
    if not output_dir:
        output_dir = os.path.split(avro_file_path)[0]
    else:
        try:
            os.makedirs(output_dir, exist_ok=False)
        except:
            print("Già convertito - skipping")
            return
        
    # Read Avro file
    reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
    data= next(reader)
    
    # BVP
    bvp = data["rawData"]["bvp"]
    timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"])) for i in range(len(bvp["values"]))]
    with open(os.path.join(output_dir, 'bvp.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["unix_timestamp", "bvp"])
        writer.writerows([[ts, bvp] for ts, bvp in zip(timestamp, bvp["values"])])
        
    # Systolic peaks
    sps = data["rawData"]["systolicPeaks"]
    with open(os.path.join(output_dir, 'systolic_peaks.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["systolic_peak_timestamp"])
        writer.writerows([[sp] for sp in sps["peaksTimeNanos"]])
    
    reader.close()
    
    if delete_avro_after:
        try:
            os.remove(avro_file_path)
        except:
            pass