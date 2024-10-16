import os
import pandas as pd

def estimate_hr(subject_dir, peaks_file='systolic_peaks.csv', save_to_file=True, delete_peaks_file_after=False):

    try:
        sys_peaks = pd.read_csv(os.path.join(subject_dir, peaks_file), sep=',')
    except Exception as e:
        print(e)
        raise FileNotFoundError("No " + peaks_file + " file found in the subject dir: " + subject_dir)
    
    sys_peaks.systolic_peak_timestamp = (sys_peaks.systolic_peak_timestamp / 10**3).astype('uint64')
    peaks = sys_peaks.systolic_peak_timestamp

    heart_rates = []
    for i in range(1, len(peaks)):
        hr = 60 / ((peaks[i] - peaks[i-1]) / 10**6)
        heart_rates.append(hr)
    
    hr = pd.DataFrame(data= {'unix_timestamp':peaks[:-1], 'hr':heart_rates})
    
    if save_to_file:
        hr.to_csv(os.path.join(subject_dir, 'hr.csv'), index=False)
    
    if delete_peaks_file_after:
        try:
            os.remove(os.path.join(subject_dir, peaks_file))
        except:
            pass
    
    return hr