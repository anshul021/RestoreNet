import random
import soundfile as sf
import numpy as np
import os

from quick_load_soundfile import load_audio_fast_stereo

print("Beginning of script")

input_path = r"D:\Rudra Veena\Waveform\Batched Training Audio\33_8_24_33.wav"
waveform, sr = load_audio_fast_stereo(input_path)

print(f"Loaded waveform shape: {waveform.shape}, Sample rate: {sr} Hz")

audio_length = 184184 # samples
# Trim to desired length - waveform is (samples, channels), so slice first dimension
waveform = waveform[:audio_length, :]

# Save the ground truth version (without holes) first
ground_truth_path = r"C:\Users\AnshulRaghav\Desktop\audio-inpainting-diffusion\trimmed_ground_truth_5.wav"
ground_truth_dir = os.path.dirname(ground_truth_path)
os.makedirs(ground_truth_dir, exist_ok=True)
sf.write(ground_truth_path, waveform, sr, format="WAV", subtype="PCM_16")
print(f"Saved ground truth to: {ground_truth_path}")

# Add 4 holes, each 100 milliseconds long
num_holes = 4
hole_length_ms = 100
hole_length_s = hole_length_ms / 1000
hole_length_samples = int(hole_length_s * sr)

# Calculate evenly spaced positions for the holes
# Leave some margin at the start and end
margin = hole_length_samples
available_length = waveform.shape[0] - 2 * margin
hole_spacing = available_length / (num_holes + 1)

hole_positions = []
for i in range(num_holes):
    start_time = margin + int((i + 1) * hole_spacing)
    end_time = start_time + hole_length_samples
    waveform[start_time:end_time, :] = 0.0
    hole_positions.append((start_time, end_time))
    print(f"Hole {i+1}: samples {start_time} to {end_time}")

print(f"After processing waveform shape: {waveform.shape}, Sample rate: {sr} Hz")

# Create output directory if it doesn't exist
output_path = r"C:\Users\AnshulRaghav\Desktop\audio-inpainting-diffusion\trimmed_with_hole_5.wav"
output_dir = os.path.dirname(output_path)
os.makedirs(output_dir, exist_ok=True)

# soundfile expects (samples, channels) format, which is what we already have
print(f"Final waveform shape for saving (with holes): {waveform.shape}")

# Save the version with holes
sf.write(output_path, waveform, sr, format="WAV", subtype="PCM_16")
print(f"Saved audio with holes to: {output_path}")

mask = np.ones((waveform.shape[0],), dtype=np.float32)
# Set all 4 holes to 0 in the mask
for start_time, end_time in hole_positions:
    mask[start_time:end_time] = 0
mask_path = r"C:\Users\AnshulRaghav\Desktop\audio-inpainting-diffusion\trimmed_with_hole_mask_5.npy"
os.makedirs(os.path.dirname(mask_path), exist_ok=True)
np.save(mask_path, np.array(mask))