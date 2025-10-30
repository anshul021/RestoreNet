import librosa
import soundfile as sf
import numpy as np

def load_audio_fast_mono(fp, dtype="float32"):
    """
    Load audio file and convert to mono by averaging channels.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate
    y, sr = librosa.load(fp, sr=None, mono=False, dtype=dtype)
    
    # If stereo, convert to mono by averaging channels
    if y.ndim > 1:
        y = np.mean(y, axis=0, keepdims=True)
    
    return y.squeeze(), sr

def load_audio_fast_stereo(fp, dtype="float32"):
    """
    Load audio file and keep stereo channels.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate, keep channels
    y, sr = librosa.load(fp, sr=None, mono=False, dtype=dtype)
    
    return y, sr

def load_audio_fast_mono_soundfile(fp, dtype="float32"):
    """
    Alternative implementation using soundfile directly for potentially faster loading.
    Load audio file and convert to mono by averaging channels.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate
    y, sr = sf.read(fp, dtype=dtype)
    
    # If stereo, convert to mono by averaging channels
    if y.ndim > 1:
        y = np.mean(y, axis=1, keepdims=True)
    
    return y.squeeze(), sr

def load_audio_fast_stereo_soundfile(fp, dtype="float32"):
    """
    Alternative implementation using soundfile directly for potentially faster loading.
    Load audio file and keep stereo channels.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate, keep channels
    y, sr = sf.read(fp, dtype=dtype)
    
    return y, sr
