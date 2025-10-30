import soundfile as sf
import numpy as np

def load_audio_fast_mono(fp, dtype="float32"):
    """
    Load audio file and convert to mono by averaging channels.
    Uses soundfile directly for maximum speed.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate using soundfile (much faster than librosa)
    y, sr = sf.read(fp, dtype=dtype)
    
    # If stereo, convert to mono by averaging channels
    if y.ndim > 1:
        y = np.mean(y, axis=1)  # Remove keepdims=True
    
    return y.squeeze(), sr

def load_audio_fast_stereo(fp, dtype="float32"):
    """
    Load audio file and keep stereo channels.
    Uses soundfile directly for maximum speed.
    Returns audio data and sample rate.
    """
    # Load audio at native sample rate, keep channels
    y, sr = sf.read(fp, dtype=dtype)
    
    return y, sr
