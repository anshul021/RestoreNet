import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt
from quick_load import load_audio_fast_stereo

def create_spectrogram(audio_path, output_image_path):
    print(f"Loading audio file: {audio_path}")
    file, sr = load_audio_fast_stereo(audio_path)
    print(file.shape)
    file = file[0][0:44100*5] # Only include first 5 seconds
    print(f"Audio loaded. Sample rate: {sr}, Length: {len(file)/sr:.2f} seconds")

    print("Computing STFT...")
    S = librosa.stft(file)
    S_db = librosa.amplitude_to_db(abs(S))

    print("Generating spectrogram plot...")
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    print(f"Saving spectrogram image to: {output_image_path}")
    plt.savefig(output_image_path)
    plt.close()
    print(f"Spectrogram saved to {output_image_path}")

if __name__ == "__main__":
    create_spectrogram(r"D:\Rudra Veena\Waveform\Batched Training Audio\1_5_17_23.wav", r"D:\Rudra Veena\1_5_17_23.png")