# pip install soxr soundfile
from quick_load import load_audio_fast_stereo
import numpy as np
import soxr
import soundfile as sf

def resample_audio(input_path, output_path, target_sr):
    waveform, orig_sr = load_audio_fast_stereo(input_path)  # shape (C, N)
    print(f"Original sample rate: {orig_sr}, waveform shape: {waveform.shape}")

    C, N = waveform.shape

    if orig_sr == target_sr:
        sf.write(output_path, waveform.T, target_sr, format="WAV", subtype="PCM_16")
        print(f"No resample needed. Saved to {output_path}")
        return

    # soxr expects time on a specific axis. We put time on axis 0: shape (N, C)
    x = waveform.T.astype(np.float32, copy=False)

    # High quality, time axis is 0
    y = soxr.resample(x, orig_sr, target_sr, quality="HQ")

    # y is (N_out, C)
    sf.write(output_path, y, target_sr, format="WAV", subtype="PCM_16")
    print(f"Resampled {input_path} from {orig_sr} Hz to {target_sr} Hz and saved to {output_path}")

def resample_audio_batch(input_paths, output_paths, target_sr):
    assert len(input_paths) == len(output_paths), "Input and output path lists must be the same length."
    for inp, outp in zip(input_paths, output_paths):
        resample_audio(inp, outp, target_sr)


if __name__ == "__main__":

    input_files = [
        f"D:/Rudra Veena/Waveform/Spliced Training Audio/{i}.wav" for i in range(1, 21)
    ]

    #input_path = r"D:\Rudra Veena\Waveform\Raw Training Audio\1.wav"
    #output_path = r"D:\Rudra Veena\Waveform\Raw Training Audio\1_downsampled.wav"
    target_sr = 44100
    #resample_audio(input_path, output_path, target_sr)
    resample_audio_batch(input_files, input_files, target_sr)
