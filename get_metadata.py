from mutagen.wave import WAVE
import os
import pandas as pd

def get_info(path):
    audio = WAVE(path)
    channels = audio.info.channels
    sample_rate = audio.info.sample_rate
    duration = audio.info.length
    #artist = audio.tags.get("\xa9ART")[0]
    bit_depth = audio.info.bits_per_sample
    return channels, sample_rate, duration, bit_depth

#print(get_info("D:/Rudra Veena/Training Audio/Ustad Asad Ali Khan - Raga Darbari - Rudra Veena - Dhrupad - Pandit Gopal Das Panse - Pakhawaj.m4a"))

folder = r"D:\Rudra Veena\Waveform\Clean Training Audio"

df = pd.read_excel(r"G:\My Drive\Rudra Veena\Metadata\Selected Data.xlsx")

data = {
    "File Name": [],
    "Channels": [],
    "Sample Rate": [],
    "Duration": [],
    "Bit Depth": []
}

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    info = get_info(file_path)
    data["File Name"].append(filename)
    data["Channels"].append(info[0])
    data["Sample Rate"].append(info[1])
    data["Duration"].append(info[2]/60)
    data["Bit Depth"].append(info[3])

meta = pd.DataFrame(data)
meta.index = df.index
df = pd.concat([df, meta], axis=1)
print(df)

df.to_excel(r"G:\My Drive\Rudra Veena\Metadata\Audio Metadata.xlsx", index=False)