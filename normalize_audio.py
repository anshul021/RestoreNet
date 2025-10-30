import soundfile as sf
import numpy as np
from quick_load import load_audio_fast_stereo
import torchaudio
import torch
import pandas as pd

TARGET_PEAK = 10 ** (-1/20)  # -1 dBFS

def check_for_dc_offset(input_path):
    # Load audio
    raw_waveform, actual_sampling_rate = load_audio_fast_stereo(input_path)
    print(f"Loaded {input_path} with shape: {raw_waveform.shape} at {actual_sampling_rate} Hz")

    # Compute mean across all channels
    dc_offset = np.mean(raw_waveform, axis=1)  # shape (channels,)

    print(f"DC offset per channel: {dc_offset}")
    return dc_offset

check_for_dc_offset_batch = lambda paths: [check_for_dc_offset(p) for p in paths]

def normalize(input_path, output_path, desired_sampling_rate):
    # Load audio
    # TODO: add a setting to modify bit depth (e.g., 16-bit, 24-bit)
    raw_waveform, actual_sampling_rate = load_audio_fast_stereo(input_path)
    print(f"Loaded {input_path} with shape: {raw_waveform.shape} at {actual_sampling_rate} Hz")

    # Resample if needed
    if actual_sampling_rate != desired_sampling_rate:
        print(f"Desired sampling rate is {desired_sampling_rate} Hz, actual sampling rate is {actual_sampling_rate} Hz")
        resampler = torchaudio.transforms.Resample(orig_freq=actual_sampling_rate, new_freq=desired_sampling_rate)
        raw_waveform_updated = torch.from_numpy(raw_waveform.T)
        raw_waveform_updated = resampler(raw_waveform_updated)
        raw_waveform = raw_waveform_updated.T.numpy()

    # Compute max abs value across all channels
    peak = np.max(np.abs(raw_waveform))
    if peak > 0:
        raw_waveform = raw_waveform * (TARGET_PEAK / peak)

    # Save back
    print(raw_waveform.shape)
    sf.write(output_path, raw_waveform.T, desired_sampling_rate, format="WAV", subtype="PCM_16")

    return TARGET_PEAK / peak  # normalization factor

def normalize_batch(input_paths, output_paths, desired_sampling_rate):
    normalization_factor = []
    assert len(input_paths) == len(output_paths), "Input and output path lists must be the same length."
    print("Starting batch normalization...")
    for inp, outp in zip(input_paths, output_paths):
        print(f"Normalizing {inp} -> {outp}")
        normalization_factor.append(normalize(inp, outp, desired_sampling_rate))

    return normalization_factor

# Batch normalization for 1.wav to 20.wav
input_files = [
    f"D:/Rudra Veena/Waveform/Spliced Training Audio/{i}.wav" for i in range(21, 41)
]

output_files = [
    f"D:/Rudra Veena/Waveform/Clean Training Audio/{i}.wav" for i in range(21, 41)
]

#normalize_batch(["D:/Rudra Veena/Waveform/Spliced Training Audio/1.wav"], ["D:/Rudra Veena/Waveform/Clean Training Audio/1.wav"], 44100)
#load_audio_fast_stereo("D:/Rudra Veena/Waveform/Spliced Training Audio/1.wav")
#check_for_dc_offset_batch(input_files)

df = pd.read_excel(r"G:\My Drive\Rudra Veena\Metadata\Audio Metadata.xlsx")
df["Normalization Factor"] = normalize_batch(input_files, output_files, 44100)
df.to_excel(r"G:\My Drive\Rudra Veena\Metadata\Audio Metadata.xlsx", index=False)