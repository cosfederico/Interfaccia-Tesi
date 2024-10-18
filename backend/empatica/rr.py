import os
import numpy as np
import pywt
from scipy import signal
import pandas as pd
from scipy.ndimage import gaussian_filter1d
        
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = signal.butter(order, [low, high], btype='band', output='sos')
    return sos

def bandpass_filter(data, cutoff, fs, order=4):
    sos = butter_bandpass(cutoff[0], cutoff[1], fs, order=order)
    zi = signal.sosfilt_zi(sos) * data[0]
    y, _ = signal.sosfilt(sos, data, zi=zi)
    return y

def downsample(original_signal, factor):
    downsampled_signal = signal.resample_poly(original_signal, up=1, down=factor)
    return downsampled_signal

def find_ridge_greedy(cwt_coeffs, freqs, penalty_factor=3000, init_window=10, search_window_size=8):
    cwt = np.abs(cwt_coeffs)
    num_freqs, num_times = cwt.shape

    init_window = min(init_window, num_times)
    avg_initial_amplitudes = np.mean(cwt[:, :init_window], axis=1)

    ridge_indices = np.zeros(num_times, dtype=int)
    ridge_indices[0] = np.argmax(avg_initial_amplitudes)

    for t in range(1, num_times):
        f = ridge_indices[t - 1]   
                
        search_window = (max(0, f - search_window_size), min(num_freqs, f + search_window_size + 1))
        search_range = np.arange(*search_window)
        
        penalties = np.abs(np.arange(*search_window) - f)**2.5 / search_window[1]
        
        local_cost = np.abs(cwt[search_range, t] - cwt[f, t-1])
        penalized_cost = local_cost + local_cost * (penalties * penalty_factor)
        
        best_local_f = np.argmin(penalized_cost)
        ridge_indices[t] = search_range[best_local_f]

    ridge_freqs = freqs[ridge_indices]

    return ridge_freqs

def estimate_rr(subject_dir, fs=64, bvp_file='bvp.csv', respiratory_band=(0.1, 0.5), filter_order=4, downsampling_factor=8, wavelet='morl', penalty_factor=3000, search_window_size=8, init_window=None, skip_start=False, save_to_file=True, delete_bvp_file_after=False):
    
    # wavelet = 'morl' # 'cmor0.5-5.0' # 'cmor0.25-8.0' # 'cmor1.25-1.0'
    
    if not init_window:
        init_window = fs // downsampling_factor
    
    ## IMPORTS

    try:
        bvp = pd.read_csv(os.path.join(subject_dir, bvp_file), sep=',')
    except Exception as e:
        print(e)
        raise FileNotFoundError("No " + bvp_file + " file found in the subject dir: " + subject_dir)
    
    if skip_start:
        bvp = bvp[len(bvp)//20:]
        bvp = bvp.reset_index(drop=True)

    ## PREPROCESSING

    filtered_signal = bandpass_filter(bvp.bvp, respiratory_band, fs, order=filter_order)
    downsampled_signal = downsample(filtered_signal, downsampling_factor)

    ## CWT

    dt = 1 / fs
    scales_range = pywt.frequency2scale(wavelet, np.array(respiratory_band)*dt)
    scales = np.arange(scales_range[1], scales_range[0])
    coefficients, frequencies = pywt.cwt(downsampled_signal, scales, wavelet, sampling_period=dt, method='fft')

    if np.iscomplex(coefficients).any():
        coefficients = np.real(coefficients)
        
    ## RIDGE DETECTION

    ridge_freqs = find_ridge_greedy(coefficients, frequencies, penalty_factor=penalty_factor, 
                                                            init_window=init_window,
                                                            search_window_size=search_window_size)

    ## SAVE RESULTS

    smoothed_rr = gaussian_filter1d(ridge_freqs*60, sigma=10)
    upsampled_rr = signal.resample(smoothed_rr, len(bvp))
    rr = pd.DataFrame({"unix_timestamp":bvp.unix_timestamp, "rr":upsampled_rr})
    
    if save_to_file:
        rr.to_csv(os.path.join(subject_dir, 'rr.csv'), index=False)
    
    if delete_bvp_file_after:
        try:
            os.remove(os.path.join(subject_dir, bvp_file))
        except:
            pass
    
    return rr