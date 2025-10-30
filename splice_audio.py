import subprocess
import os
from mutagen import File
from pathlib import Path

def invert_ranges(ranges, total_duration):
    """
    Given a list of (start, end) ranges and the total duration,
    return the inverted ranges (i.e., the parts NOT in the input ranges).
    """
    if not ranges:
        return [(0, total_duration)]
    ranges = sorted(ranges)
    inv = []
    prev_end = 0
    for start, end in ranges:
        if end == None:
            end = total_duration
        if start > prev_end:
            inv.append((prev_end, start))
        prev_end = max(prev_end, end)
    if prev_end < total_duration:
        inv.append((prev_end, total_duration))
    return inv

def get_audio_duration(input_file):
    path = Path(input_file)
    audio = File(path)
    duration_sec = audio.info.length  # float seconds
    return duration_sec

def splice_audio(input_files, output_dir, segments):
    output_files = []
    for input_file in input_files:
        base_name = os.path.basename(input_file)
        file_segments = segments[base_name]
        if file_segments == []:
            print(f"No segments to remove for {input_file}, copying as is.")
            output_file = os.path.join(output_dir, base_name)
            subprocess.run([
                "ffmpeg",
                "-i", input_file,
                "-c", "copy",
                output_file
            ], check=True)
            output_files.append(output_file)
            continue
        # Always invert the ranges (crop out the segments)
        total_duration = get_audio_duration(input_file)
        file_segments = invert_ranges(file_segments, total_duration)
        temp_files = []
        for i, (start, end) in enumerate(file_segments, 1):
            duration = end - start
            temp_file = os.path.join(output_dir, f"{base_name}_part{i}.wav")
            print("temp file: "+temp_file)
            temp_files.append(temp_file)
            subprocess.run([
                "ffmpeg",
                "-ss", str(start),
                "-i", input_file,
                "-t", str(duration),
                "-c:a", "pcm_s16le",
                temp_file
            ], check=True)

        # Create a file list for ffmpeg concat
        concat_list_path = os.path.join(output_dir, f"{base_name}_concat_list.txt")
        with open(concat_list_path, 'w', encoding='utf-8') as f:
            for temp_file in temp_files:
                f.write(f"file '{temp_file}'\n")

        output_file = os.path.join(output_dir, base_name)
        ffmpeg_cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_path
        ]
        if output_file.lower().endswith('.wav'):
            ffmpeg_cmd += ["-c:a", "pcm_s16le"]
        else:
            ffmpeg_cmd += ["-c", "copy"]
        ffmpeg_cmd.append(output_file)
        subprocess.run(ffmpeg_cmd, check=True)
        output_files.append(output_file)

        # Clean up temp files
        for temp_file in temp_files:
            os.remove(temp_file)
        os.remove(concat_list_path)

    print(output_files)


input_files = [
    "D:/Rudra Veena/Waveform/Raw Training Audio/21.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/22.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/23.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/24.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/25.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/26.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/27.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/28.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/29.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/30.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/31.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/32.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/33.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/34.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/35.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/36.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/37.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/38.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/39.wav",
    "D:/Rudra Veena/Waveform/Raw Training Audio/40.wav"
]

output_dir = "D:/Rudra Veena/Waveform/Spliced Training Audio"

# Use None for the end time to indicate "to end" or "onwards"
segments_1 = {
    "1.wav":   [(35*60+33, 38*60+18)],
    "2.wav":   [(42*60+30, 43*60+0)],
    "3.wav":   [(37*60+0, 37*60+20)],
    "4.wav":   [(48*60+15, 48*60+50)],
    "5.wav":   [(55*60+45, None)],
    "6.wav":   [(32*60+40, 33*60+0), (47*60+55, None)],
    "7.wav":   [(57*60+40, None)],
    "8.wav":   [],
    "9.wav":   [],
    "10.wav":  [],
    "11.wav":  [],
    "12.wav":  [(51*60+40, None)],
    "13.wav":  [(55*60+0, None)],
    "14.wav":  [(58*60+30, None)],
    "15.wav":  [],
    "16.wav":  [(51*60+20, 51*60+46), (69*60+40, None)],
    "17.wav":  [(57*60+56, None)],
    "18.wav":  [(0, 15), (48*60+35, 49*60+15), (63*60+10, None)],
    "19.wav":  [],
    "20.wav":  [(0, 60), (69*60+5, None)]
}


segments_2 = {
    "21.wav": [(0, 1*60+0), (42*60+0, 45*60+0), (1*3600+0*60+45, None)],
    "22.wav": [(0, 0*60+5), (44*60+50, None)],
    "23.wav": [(0, 0*60+20), (1*3600+8*60+7, None)],
    "24.wav": [(0, 0*60+50), (28*60+0, None)],
    "25.wav": [(0, 12*60+0), (1*3600+20*60+40, None)],
    "26.wav": [(0, 1*60+20), (8*60+40, 9*60+0), (34*60+20, 34*60+50), (47*60+40, None)],
    "27.wav": [(0, 4*60+30), (54*60+45, None)],
    "28.wav": [(0, 0*60+20), (42*60+10, None)],
    "29.wav": [(0, 1*60+0), (14*60+45, 16*60+45), (52*60+0, 54*60+0), (1*3600+7*60+20, None)],
    "30.wav": [(0, 0*60+15), (34*60+5, 34*60+20), (46*60+50, None)],
    "31.wav": [(0, 0*60+15), (41*60+50, 42*60+2), (42*60+33, 43*60+0), (55*60+15, None)],
    "32.wav": [(0, 4*60+10), (46*60+40, 47*60+5), (1*3600+2*60+17, None)],
    "33.wav": [(0, 3*60+0), (27*60+40, 32*60+0), (59*60+10, None)],
    "34.wav": [(0, 0*60+15), (1*3600+8*60+35, None)],
    "35.wav": [(0, 0*60+30), (1*3600+8*60+0, None)],
    "36.wav": [(0, 0*60+20), (40*60+40, None)],
    "37.wav": [(0, 0*60+5), (34*60+20, None)],
    "38.wav": [(0, 0*60+5), (45*60+40, None)],
    "39.wav": [(0, 0*60+5), (1*3600+9*60+20, None)],
    "40.wav": [(0, 0*60+5), (1*3600+5*60+40, None)]
}

splice_audio(input_files, output_dir, segments_2)