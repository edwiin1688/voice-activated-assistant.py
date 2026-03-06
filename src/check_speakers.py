import torch
from qwen_tts import Qwen3TTSModel
import sys

def check_speakers():
    model_path = "models/Qwen3-TTS-12Hz-0.6B-CustomVoice"
    try:
        model = Qwen3TTSModel.from_pretrained(
            model_path, 
            device_map="cuda",
            trust_remote_code=True
        )
        raw_supported = model.model.get_supported_speakers()
        print(f"RAW_SUPPORTED: {raw_supported!r}")
        supported = model._supported_speakers_set()
        print(f"SUPPORTED_LIST: {sorted(list(supported)) if supported else None}")
        
        test_speaker = "serena"
        print(f"Testing speaker: {test_speaker!r}")
        try:
            wavs, sr = model.generate_custom_voice("你好", speaker=test_speaker)
            print(f"Success! Generated {len(wavs[0])} samples at {sr}Hz")
        except Exception as e:
            print(f"Failed to generate: {e}")
        else:
            print("No speakers found or get_supported_speakers not callable")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_speakers()
