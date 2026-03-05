"""Audio input module - Microphone capture"""

import numpy as np
import sounddevice as sd
from typing import Callable, Optional
from dataclasses import dataclass


@dataclass
class AudioConfig:
    sample_rate: int = 16000
    frame_duration_ms: int = 30
    channels: int = 1
    dtype: str = "float32"
    device: Optional[int] = None

    @property
    def frame_samples(self) -> int:
        return int(self.sample_rate * self.frame_duration_ms / 1000)


class AudioInput:
    def __init__(
        self,
        config: Optional[AudioConfig] = None,
        callback: Optional[Callable[[np.ndarray], None]] = None,
    ):
        self.config = config or AudioConfig()
        self.callback = callback
        self._stream: Optional[sd.InputStream] = None
        self._is_running = False

    def list_devices(self):
        print("Available audio devices:")
        print(sd.query_devices())

    def start(self):
        if self._is_running:
            return

        try:
            devices = sd.query_devices()
            if devices is None or (
                isinstance(devices, dict) and devices.get("max_input_channels", 0) == 0
            ):
                print("[AUDIO] No input devices available!")
                print("Run with --list-devices to see available devices")
                return False
        except Exception as e:
            print(f"[AUDIO] Error querying devices: {e}")
            return False

        try:
            self._stream = sd.InputStream(
                samplerate=self.config.sample_rate,
                channels=self.config.channels,
                dtype=self.config.dtype,
                blocksize=self.config.frame_samples,
                device=self.config.device,
                callback=self._audio_callback,
            )
            self._stream.start()
            self._is_running = True
            return True
        except Exception as e:
            print(f"[AUDIO] Failed to start audio stream: {e}")
            return False

    def stop(self):
        if not self._is_running:
            return

        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._is_running = False

    def _audio_callback(
        self, indata: np.ndarray, frames: int, time, status: sd.CallbackFlags
    ):
        if status:
            print(f"[AUDIO] Status: {status}")

        audio_data = indata[:, 0].copy()

        if self.callback:
            self.callback(audio_data)

    def is_running(self) -> bool:
        return self._is_running
