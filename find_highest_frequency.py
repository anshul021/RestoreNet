import numpy as np
import soundfile as sf
import sys

"""
Usage:
    python find_highest_frequency.py <audio_file>
"""

def find_highest_frequency(audio_path):
    audio, sr = sf.read(audio_path)
    if audio.ndim > 1:
        audio = audio[:, 0]  # Use first channel if stereo
    fft = np.fft.rfft(audio)
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    max_freq = freqs[np.argmax(np.abs(fft))]
    print(f"Highest energy frequency: {max_freq:.2f} Hz (Sample rate: {sr} Hz)")
    return max_freq

if __name__ == "__main__":
    find_highest_frequency(r"D:\Rudra Veena\Waveform\Batched Training Audio\1_1_0_8.wav")
