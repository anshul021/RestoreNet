from yt_dlp import YoutubeDL
import os
import pandas as pd
import json

print("Starting download script...")

def download_video(output_dir, url_list, train_or_test):
    print("Directory exists?: "+str(os.path.exists(output_dir)))

    yt_data = pd.read_excel(r"G:\My Drive\Rudra Veena\Metadata\Selected Data.xlsx")

    # Convert to set for O(1) lookup instead of O(n) list lookup
    downloaded_urls = set(yt_data["URL"].tolist())

    # Get the current max number in the folder (for sequential naming)
    existing_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    numbers = []
    for f in existing_files:
        name, _ = os.path.splitext(f)
        try:
            numbers.append(int(name))
        except ValueError:
            continue
    next_number = max(numbers) + 1 if numbers else 1

    # Collect all new rows to append to dataframe
    new_rows = []

    for url in url_list:
        if url in downloaded_urls:
            print("Already downloaded!")
            continue

        # Set output template to use the next available number
        outtmpl = f"{output_dir}/{{number}}"
        opts = {
            "format": "bestaudio*/*",  # prefer actual audio streams first
            "outtmpl": outtmpl.replace("{number}", str(next_number)),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "0",
                },
                {"key": "FFmpegMetadata"},
            ],
            "postprocessor_args": ["-sample_fmt", "s16"],
            # Workarounds for SABR and region gating
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]  # try android first
                }
            },
            # Optional but often helpful if videos are age or region gated:
            # "cookiesfrombrowser": ("chrome",),  # or ("edge",) depending on your browser
        }

        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title")
            author = info.get("uploader")
            duration_hours = info.get("duration")/3600
            ydl.download([url])

        new_rows.append({
            "URL": url,
            "Number": next_number, 
            "Title": title,
            "Author": author,
            "Duration (hours)": duration_hours,
            "Train or Test": train_or_test
        })
        next_number += 1

    # Append all new rows at once instead of one-by-one
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        yt_data = pd.concat([yt_data, new_df], ignore_index=True)
        yt_data.to_excel(r"G:\My Drive\Rudra Veena\Metadata\Selected Data.xlsx", index=False)

# storing audio on Desktop instead of Google Drive
training_dir = r"D:\Rudra Veena\Waveform\Raw Training Audio"

with open("training_urls.json", "r") as f:
    url_list = json.load(f)

print(url_list)
#download_video(training_dir, url_list, "train")

download_video("D:/Rudra Veena/General Test Audios", ["https://www.youtube.com/watch?v=DmO8NYF6a9E"], "train")