import librosa
import numpy as np
from quick_load import load_audio_fast_stereo

# Load stereo file, preserving both channels
for i in range(1, 21):
    y, sr = load_audio_fast_stereo("D:/Rudra Veena/Waveform/Raw Training Audio/"+str(i)+".wav")
    print("Reading file "+"D:/Rudra Veena/Waveform/Raw Training Audio/"+str(i)+".wav")
    print(y.shape)
    print(f"Sampling rate: {sr}")
    print(f"Duration (s): {len(y)/sr:.2f}")

    # y will be shape (2, n_samples): y[0] = left, y[1] = right
    left = y[0]
    right = y[1]

    corr = np.corrcoef(left, right)[0, 1]
    print(f"Correlation between L and R: {corr:.3f}")

    mid = (left + right) / 2
    side = (left - right) / 2
    ratio = np.mean(side**2) / np.mean(mid**2)
    print(f"Side/Mid energy ratio: {ratio:.3f}")