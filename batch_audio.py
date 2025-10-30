from quick_load import load_audio_fast_stereo
import torchaudio
import torch
import os
import math
import random
import pandas as pd

def batch_audio(input_file, output_dir):
    y, sr = load_audio_fast_stereo(input_file)  # y shape (2, n_samples), float32
    n_ch, n_samp = y.shape
    input_length_mins = n_samp/sr/60

    print(y.shape)
    print(f"Sampling rate: {sr}")
    print(f"Duration (s): {input_length_mins:.2f}")

    batches = batch_size(input_length_mins)
    print(batches)
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    for i in range(len(batches)):
        batch_start = batches[i]["start"]*60*sr
        batch_end = batches[i]["end"]*60*sr
        batch_length = batches[i]["size"]
        print(str(batches[i])+" "+str(batch_length))
        batch = y[:, math.ceil(batch_start):math.floor(batch_end)]  # shape (2, num_samples)
        print(batch.shape)
        print("Batch duration (s): " + str(batches[i]))

        torchaudio.save(
            output_file.replace(".wav", f"_{i+1}_{round(batches[i]["start"])}_{round(batches[i]["end"])}.wav"),
            torch.from_numpy(batch),
            sr,
            encoding="PCM_S",
            bits_per_sample=16
        )

def batch_size(n, min_len=5, max_len=10):
    """
    Partition a continuous extent of length n into random groups,
    each between 5 and 10 (inclusive), with 50% overlap.
    
    Returns a list of dicts: {"start": float, "size": float, "end": float}
    so each group covers [start, end). The next group's start is
    previous_start + size/2, giving 50% overlap.
    """

    groups = []
    start = 0.0
    eps = 1e-9

    while True:
        remaining = n - start
        if remaining < 5 - eps:
            # Numerical safety: if we somehow undershoot, merge into the last group
            if not groups:
                raise RuntimeError("Internal error: no groups but remaining < 5.")
            g = groups.pop()
            # Extend the last group so it ends at n while keeping size in [5, 10]
            new_size = (n - g["start"])
            if not (5 - eps <= new_size <= 10 + eps):
                raise RuntimeError("Unable to fix last group to valid size.")
            groups.append({"start": g["start"], "size": new_size, "end": n})
            break

        if 5 - eps <= remaining <= 10 + eps:
            # Final group fits perfectly
            size = remaining
            groups.append({"start": start, "size": size, "end": start + size})
            break

        # Choose a size t in [5, ub], where ub ensures we still have at least 5 left
        # for the next final window after we advance by t/2
        ub = min(10.0, 2.0 * (remaining - 5.0))
        if ub < 5 - eps:
            # If ub fell below 5, then the final window should be now
            size = remaining
            if not (5 - eps <= size <= 10 + eps):
                # If that fails, adjust the previous group
                if not groups:
                    raise RuntimeError("Cannot satisfy constraints with n given.")
                g = groups.pop()
                # Recompute this last group to end exactly at n with a valid size
                size = n - g["start"]
                if not (5 - eps <= size <= 10 + eps):
                    raise RuntimeError("Unable to adjust to valid final size.")
                groups.append({"start": g["start"], "size": size, "end": n})
                break
            groups.append({"start": start, "size": size, "end": start + size})
            break

        size = random.uniform(5.0, ub)
        groups.append({"start": start, "size": size, "end": start + size})
        start += size / 2.0  # 50% overlap hop

    return groups

batch_audio_group = lambda input_files, output_dir: [batch_audio(f, output_dir) for f in input_files]

input_files = [
    f"D:/Rudra Veena/Waveform/Spliced Training Audio/{i}.wav" for i in range(21, 41)
]

output_dir = "D:/Rudra Veena/Waveform/Batched Training Audio"

groups = batch_audio_group(input_files, output_dir)
df = pd.DataFrame(groups)
print(df)
df.to_excel(r"G:\My Drive\Rudra Veena\Metadata\Batch Metadata", index=False)
#print(batch_size(46.138))
#batch_audio("D:/Rudra Veena/Waveform/Clean Training Audio/1.wav", "D:/Rudra Veena/Waveform/Batched Training Audio")
#split_balanced("D:/Rudra Veena/Waveform/Clean Training Audio/3.wav")