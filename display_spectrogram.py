import numpy as np
import matplotlib.pyplot as plt

# Path to the spectrogram file
data_path = "D:/Rudra Veena/Spectrogram/Clean Spectrograms/1.npz"

data = np.load(data_path)
mag_log = data['mag_log']

plt.figure(figsize=(10, 4))
plt.imshow(mag_log, aspect='auto', origin='lower', cmap='magma')
plt.title('Log-Magnitude Spectrogram')
plt.xlabel('Frame')
plt.ylabel('Frequency Bin')
plt.colorbar(label='Log Magnitude')
plt.tight_layout()
plt.show()
