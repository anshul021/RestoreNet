# Rudra Veena Audio Processing Pipeline

This project provides a pipeline for processing audio data, starting from downloading YouTube videos to preparing NumPy arrays for machine learning or analysis. The workflow is modular, with each step handled by a dedicated script.

## Workflow Overview

1. **Download YouTube Videos**
   - **Script:** `download_youtube_videos.py`
   - **Purpose:** Downloads audio tracks from a list of YouTube URLs using `yt-dlp`.
   - **Input:** JSON files containing YouTube URLs (e.g., `training_urls.json`, `evaluation_urls.json`).
   - **Output:** Audio files (typically in MP3 format) saved to the local directory.

2. **Splice Audio**
   - **Script:** `splice_audio.py`
   - **Purpose:** Removes unwanted sections (e.g., silence, noise, irrelevant content) and splits audio into smaller, uniform chunks (e.g., 10-second clips).
   - **Input:** Raw downloaded audio files.
   - **Output:** Cleaned and chunked audio files, each containing a relevant segment.

3. **Normalize Audio**
   - **Script:** `normalize_audio.py`
   - **Purpose:** Normalizes the loudness of each audio chunk to a consistent level and modifies the sample rate.
   - **Input:** Spliced audio files.
   - **Output:** Normalized audio files, ready for further processing.

4. **Cut Audio into Chunks**
   - **Script:** `batch_audio.py`
   - **Purpose:** Splits normalized audio files into smaller, uniform chunks (e.g., 10-second segments) for easier processing and model training.
   - **Input:** Normalized audio files.
   - **Output:** Audio chunks (WAV or MP3), each containing a segment of the original file.

5. **Convert Audio to NumPy Arrays**
   - **Script:** `wav_to_npy.py`
   - **Purpose:** Converts each normalized audio chunk (WAV/MP3) into a NumPy array and saves it as a `.npy` file for fast loading in Python workflows.
   - **Input:** Normalized audio chunks (WAV or MP3).
   - **Output:** `.npy` files containing audio data as NumPy arrays.

## Additional Scripts and Helpers

- `channel_similarity.py`: Computes the correlation between left and right stereo channels to check for similarity or phase issues.
- `display_spectrogram.py`: Generates and displays spectrograms for audio files to visualize frequency content over time.
- `get_metadata.py`: Extracts metadata (e.g., duration, sample rate, channels) from audio files and can update metadata spreadsheets.
- `baseline_model.ipynb`: Jupyter notebook for prototyping, training, or evaluating baseline machine learning models on the processed audio data.
- `quick_load.py`: Provides fast audio loading functions using `torchaudio` or similar libraries, with options for mono or stereo output.
- `test.py`, `test.json`: Scripts and data for sanity checks, ensuring each processing step works as expected.
- `resample_audio.py`: Resamples audio files to a specified sampling rate and saves the result. Useful for preparing data for models that require a specific sample rate.
- `find_highest_frequency.py`: Analyzes an audio file and prints the frequency (in Hz) with the highest energy using FFT. Usage: `python find_highest_frequency.py <audio_file>`

## Data and Helper Files

- `audio_metadata.xlsx`: Spreadsheet for tracking and annotating audio metadata (e.g., file names, durations, notes).
- `training_urls_formatted.json`, `training_urls.json`, `evaluation_urls.json`: JSON files containing YouTube URLs for training and evaluation splits.

## Usage

1. **Install dependencies in a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   pip install -r requirements.txt
   ```
2. **Run each script in order:**
   - Download audio: `python download_youtube_videos.py`
   - Splice and chunk: `python splice_audio.py`
   - Normalize: `python normalize_audio.py`
   - Cut into chunks: `python batch_audio.py`
   - Convert to NumPy: `python wav_to_npy.py`
3. **Resample audio files as needed:**
   - `python resample_audio.py <input_path> <output_path> <target_sr>`
4. **Find the highest frequency in an audio file:**
   - `python find_highest_frequency.py <audio_file>`
5. **Use helper and sanity check scripts** as needed to verify data integrity and inspect results.

## Notes
- Place all scripts and data files in the project directory.
- Adjust file paths in scripts as needed for your environment.
- See individual script files for more detailed usage instructions.

---

For questions or contributions, please open an issue or pull request.
