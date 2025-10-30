import numpy as np
import os
from quick_load import load_audio_fast_stereo

input_dir = r"D:\Rudra Veena\Waveform\Batched Training Audio"
output_dir = r"D:\Rudra Veena\Waveform\npy Training Audio"

for filename in os.listdir(input_dir):
    output_path = os.path.join(output_dir, os.path.basename(filename) + ".npy")
    if os.path.exists(output_path):
        continue
    print("Converting file: " + filename)
    full_path = os.path.join(input_dir, filename)
    y, sr = load_audio_fast_stereo(full_path, dtype="float32")
    print(y.shape)
    print(sr)
    np.save(output_path, y)