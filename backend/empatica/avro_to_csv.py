from avro.datafile import DataFileReader
from avro.io import DatumReader
import os
import json
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

    bvp, sps, eda = None, None, None

    try:
        while True:
            data= next(reader)
            if bvp is None:    
                bvp = data["rawData"]["bvp"]
            else:
                bvp["values"] += data["rawData"]["bvp"]["values"]

            if sps is None:    
                sps = data["rawData"]["systolicPeaks"]     
            else:
                sps["peaksTimeNanos"] += data["rawData"]["systolicPeaks"]["peaksTimeNanos"]

            if eda is None:               
                eda = data["rawData"]["eda"]
            else:
                eda["values"] += data["rawData"]["eda"]["values"]
            
    except StopIteration:
        pass
            
    timestamp = [round(bvp["timestampStart"] + i * (1e6 / bvp["samplingFrequency"])) for i in range(len(bvp["values"]))]
    with open(os.path.join(output_dir, 'bvp.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["unix_timestamp", "bvp"])
        writer.writerows([[ts, bvp] for ts, bvp in zip(timestamp, bvp["values"])])
        
    with open(os.path.join(output_dir, 'systolic_peaks.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["systolic_peak_timestamp"])
        writer.writerows([[sp] for sp in sps["peaksTimeNanos"]])
            
    timestamp = [round(eda["timestampStart"] + i * (1e6 / eda["samplingFrequency"]))
        for i in range(len(eda["values"]))]
    with open(os.path.join(output_dir, 'eda.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["unix_timestamp", "eda"])
        writer.writerows([[ts, eda] for ts, eda in zip(timestamp, eda["values"])])

    reader.close()
    
    with open(os.path.join(output_dir, 'fs.json'), 'w') as f:
        json.dump({"bvp": bvp["samplingFrequency"], "eda": eda["samplingFrequency"]}, f, indent=4)
    
    if delete_avro_after:
        try:
            os.remove(avro_file_path)
        except:
            pass