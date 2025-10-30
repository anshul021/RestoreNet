import os
import glob
import random
import numpy as np
import soundfile as sf
from quick_load import load_audio_fast_mono

# Input and output directories
in_dir = "D:/Rudra Veena/Waveform/Clean Training Audio"
out_dir = "D:/Rudra Veena/Waveform/Noisy Training Audio"


def add_awgn(signal, snr_db):
    """Additive White Gaussian Noise at a given SNR (dB)."""
    sig_power = np.mean(signal ** 2)
    noise = np.random.randn(len(signal))
    noise_power = np.mean(noise ** 2)
    k = np.sqrt(sig_power / (noise_power * 10 ** (snr_db / 10)))
    return signal + k * noise

def split_and_add_noise(signal, sampling_rate, snr_list, segment_minutes=5):
    """
    Split the signal into N segments (each segment_minutes long),
    and add white noise with a different SNR from snr_list to each segment.
    """
    segment_samples = segment_minutes * 60 * sampling_rate
    total_samples = len(signal)
    segments = []
    snr_used = []
    for i, start in enumerate(range(0, total_samples, segment_samples)):
        end = min(start + segment_samples, total_samples)
        snr = snr_list[i % len(snr_list)]
        noisy = add_awgn(signal[start:end], snr)
        segments.append(noisy)
        snr_used.append(snr)
    return np.concatenate(segments), snr_used

# Process each file
for fp in glob.glob(os.path.join(in_dir, "*.wav")):
    print(f"Processing {fp}")
    # Load audio
    normalized_waveform, sampling_rate = load_audio_fast_mono(fp) # TODO: find a way to keep stereo

    print("Loaded audio with shape: "+str(normalized_waveform.shape))


    # Determine number of 5-min segments
    segment_minutes = 5
    segment_samples = segment_minutes * 60 * sampling_rate
    total_samples = len(normalized_waveform)
    num_segments = (total_samples + segment_samples - 1) // segment_samples

    # Generate random SNRs between 10 and 20 dB for each segment
    snr_list = [random.uniform(10, 20) for _ in range(num_segments)]

    # Add noise with different SNRs every 5 minutes
    noisy_waveform, snrs_used = split_and_add_noise(normalized_waveform, sampling_rate, snr_list, segment_minutes=segment_minutes)

    print("Added noise, new shape: "+str(noisy_waveform.shape))

    # Build output filename
    base = os.path.splitext(os.path.basename(fp))[0]
    snr_str = "_".join([f"{s:.0f}" for s in snrs_used])
    output_path = os.path.join(out_dir, f"{base}_snrs_{snr_str}.wav")

    # Save as WAV
    sf.write(output_path, noisy_waveform, sampling_rate)
    print(f"Saved {output_path}")
    print(f"Added noise with SNRs (per 5 min): {snrs_used}")