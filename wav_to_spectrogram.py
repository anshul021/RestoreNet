import os
import numpy as np
from quick_load import load_audio_fast_mono
import torchaudio
import torch

# Target spectrogram hyperparameters
# TODO: experiment with these values
N_FFT = 1024
WIN_LENGTH = 1024
HOP_LENGTH = 256
WINDOW = "hann"  # Hann window

def waveform_to_spectrogram_and_save(normalized_waveform, sampling_rate, output_path):
    """
    Convert a normalized waveform (1D numpy array or torch tensor) to a spectrogram using torch/torchaudio and save as .npz.
    """

    # normalized_waveform is always a 1D numpy array (float32) from quick_load.py
    converted_waveform = torch.from_numpy(normalized_waveform).float().unsqueeze(0)  # (1, n_samples)

    # Compute spectrogram (complex STFT)
    S = torch.stft(
        converted_waveform,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        win_length=WIN_LENGTH,
        window=torch.hann_window(WIN_LENGTH, periodic=True, device=converted_waveform.device),
        center=True,
        pad_mode="reflect",
        normalized=False,
        onesided=True,
        return_complex=True,
    )
    S = S.squeeze(0)  # (freq, frames)

    mag_log = torch.log1p(torch.abs(S)).cpu().numpy().astype(np.float32)
    phase = torch.angle(S).cpu().numpy().astype(np.float32)

    np.savez_compressed(
        output_path,
        mag_log=mag_log,
        phase=phase,
        sr=np.int32(sampling_rate),
        n_fft=np.int32(N_FFT),
        hop_length=np.int32(HOP_LENGTH),
        win_length=np.int32(WIN_LENGTH),
        window=np.bytes_(WINDOW),
    )
    print(f"Saved spectrogram to {output_path}, shape={mag_log.shape}")

def files_to_spectrograms(file_list, out_dir):
    """
    Convert a list of stereo 44.1 kHz audio files to log-magnitude + phase spectrograms.
    Each output is saved as a compressed .npz in out_dir.
    """
    os.makedirs(out_dir, exist_ok=True)

    for input_path in file_list:
        try:
            print("Loading "+input_path)
            normalized_waveform, sampling_rate = load_audio_fast_mono(input_path)

            # Build output filename
            base = os.path.splitext(os.path.basename(input_path))[0]
            out_path = os.path.join(out_dir, f"{base}.npz")

            waveform_to_spectrogram_and_save(normalized_waveform, sampling_rate, out_path)

        except Exception as e:
            print(f"Failed on {input_path}: {e}")


if __name__ == "__main__":
    print("Beginning spectrogram conversion...")
    input_files = [
        r"D:\Rudra Veena\Waveform\Batched Training Audio\1_7_25_31.wav"
    ]
    output_dir = "D:/Rudra Veena/Spectrogram/Noisy Spectrograms"

    files_to_spectrograms(input_files, output_dir)