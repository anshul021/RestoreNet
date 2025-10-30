import time
import os

def test_loading_speed():
    """Test different loading methods to find the fastest"""
    
    test_file = r"D:\Rudra Veena\Waveform\Batched Training Audio\37_8_23_31.wav"
    
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return
    
    print("=== Audio Loading Speed Test ===")
    
    # Test 1: Soundfile (should be fastest)
    print("\n1. Testing soundfile (direct)...")
    try:
        from quick_load_fast import load_audio_fast_stereo
        start_time = time.time()
        waveform, sr = load_audio_fast_stereo(test_file)
        soundfile_time = time.time() - start_time
        print(f"Soundfile time: {soundfile_time:.3f} seconds")
        print(f"Audio shape: {waveform.shape}, Sample rate: {sr}")
    except Exception as e:
        print(f"Soundfile failed: {e}")
        soundfile_time = None
    
    # Test 2: Librosa (your current method)
    print("\n2. Testing librosa...")
    try:
        from quick_load_librosa import load_audio_fast_stereo as librosa_load
        start_time = time.time()
        waveform, sr = librosa_load(test_file)
        librosa_time = time.time() - start_time
        print(f"Librosa time: {librosa_time:.3f} seconds")
        print(f"Audio shape: {waveform.shape}, Sample rate: {sr}")
    except Exception as e:
        print(f"Librosa failed: {e}")
        librosa_time = None
    
    # Test 3: Torchaudio (original)
    print("\n3. Testing torchaudio...")
    try:
        from quick_load import load_audio_fast_stereo as torch_load
        start_time = time.time()
        waveform, sr = torch_load(test_file)
        torch_time = time.time() - start_time
        print(f"Torchaudio time: {torch_time:.3f} seconds")
        print(f"Audio shape: {waveform.shape}, Sample rate: {sr}")
    except Exception as e:
        print(f"Torchaudio failed: {e}")
        torch_time = None
    
    # Summary
    print("\n=== Performance Summary ===")
    times = [("Soundfile", soundfile_time), ("Librosa", librosa_time), ("Torchaudio", torch_time)]
    valid_times = [(name, t) for name, t in times if t is not None]
    
    if valid_times:
        fastest = min(valid_times, key=lambda x: x[1])
        print(f"Fastest method: {fastest[0]} ({fastest[1]:.3f}s)")
        
        for name, t in valid_times:
            if t is not None and fastest[1] > 0:
                speedup = t / fastest[1]
                print(f"{name}: {speedup:.1f}x slower than fastest")

if __name__ == "__main__":
    test_loading_speed()
