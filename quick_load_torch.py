import torch
import torchaudio

def load_audio_fast_mono(fp, dtype="float32"):
    # Load at native rate, keep channels
    wav, orig_sr = torchaudio.load(fp)  # shape (channels, n_samples), torch tensor
    
    wav = torch.mean(wav, dim=0, keepdim=True)

    # Convert to numpy float32 for librosa compatibility
    y = wav.numpy().astype(dtype)

    return y.squeeze(), orig_sr

def load_audio_fast_stereo(fp, dtype="float32"):
    # Load at native rate, keep channels
    wav, orig_sr = torchaudio.load(fp)  # shape (channels, n_samples), torch tensor
    
    # Convert to numpy float32 for librosa compatibility
    y = wav.numpy().astype(dtype)

    return y, orig_sr
