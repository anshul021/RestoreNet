import soundfile as sf
import os

start = 21
end = 40
folder = "D:/Rudra Veena/Waveform/Spliced Training Audio"

for i in range(start, end + 1):
    file_path = os.path.join(folder, f"{i}.wav")
    try:
        with sf.SoundFile(file_path) as f:
            print(f"{file_path}: {f.samplerate} Hz")
    except Exception as e:
        print(f"{file_path}: Error - {e}")
