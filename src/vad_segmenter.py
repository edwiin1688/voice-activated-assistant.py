"""VAD Segmenter module - Voice Activity Detection with pause detection"""

import numpy as np
from typing import Optional, Callable
from dataclasses import dataclass, field
import threading
import time


@dataclass
class VADConfig:
    silence_threshold: float = 0.5
    min_silence_duration: float = 1.0
    min_utterance_ms: int = 300
    max_utterance_s: int = 15
    sample_rate: int = 16000


@dataclass
class Utterance:
    audio: np.ndarray
    start_time: float
    end_time: float
    duration_ms: int


class VADSegmenter:
    def __init__(
        self,
        config: Optional[VADConfig] = None,
        on_utterance: Optional[Callable[[Utterance], None]] = None,
    ):
        self.config = config or VADConfig()
        self.on_utterance = on_utterance

        self._buffer: list[np.ndarray] = []
        self._buffer_lock = threading.Lock()

        self._silence_duration = 0.0
        self._speech_duration = 0.0
        self._is_speaking = False
        self._utterance_start_time: Optional[float] = None

        self._vad_model = None
        self._vad_loaded = False

    def load_vad(self):
        try:
            import torch
            import torchaudio
            from silero_vad import load_silero_vad

            self._vad_model = load_silero_vad()
            self._vad_loaded = True
        except ImportError:
            self._vad_loaded = False
        except Exception:
            self._vad_loaded = False

    def process_frame(self, audio: np.ndarray) -> bool:
        current_time = time.time()

        if not self._vad_loaded:
            is_speech = self._simple_vad(audio)
        else:
            is_speech = self._silero_vad(audio)

        with self._buffer_lock:
            if is_speech:
                if not self._is_speaking:
                    self._is_speaking = True
                    self._utterance_start_time = current_time
                    self._buffer = []
                    print("[VAD] Speech detected, recording...")

                self._buffer.append(audio.copy())
                self._speech_duration += len(audio) / self.config.sample_rate
                self._silence_duration = 0.0
            else:
                if self._is_speaking:
                    self._silence_duration += len(audio) / self.config.sample_rate

                    if self._silence_duration >= self.config.silence_threshold:
                        print(
                            f"[VAD] Silence for {self._silence_duration:.1f}s - finalizing..."
                        )
                        self._finalize_utterance()

        return is_speech

    def _simple_vad(self, audio: np.ndarray) -> bool:
        energy = np.sqrt(np.mean(audio**2))
        return energy > 0.01

    def _silero_vad(self, audio: np.ndarray) -> bool:
        if self._vad_model is None:
            return self._simple_vad(audio)

        try:
            import torch

            tensor = torch.from_numpy(audio).float()
            speech_prob = self._vad_model(tensor, self.config.sample_rate).item()
            return speech_prob > self.config.silence_threshold
        except Exception:
            return self._simple_vad(audio)

    def _finalize_utterance(self):
        if not self._buffer or self._utterance_start_time is None:
            return

        duration_ms = int(self._speech_duration * 1000)

        if duration_ms < self.config.min_utterance_ms:
            self._reset_state()
            return

        if self._speech_duration > self.config.max_utterance_s:
            self._reset_state()
            return

        audio_data = np.concatenate(self._buffer)

        utterance = Utterance(
            audio=audio_data,
            start_time=self._utterance_start_time,
            end_time=time.time(),
            duration_ms=duration_ms,
        )

        if self.on_utterance:
            self.on_utterance(utterance)

        self._reset_state()

    def _reset_state(self):
        self._buffer = []
        self._silence_duration = 0.0
        self._speech_duration = 0.0
        self._is_speaking = False
        self._utterance_start_time = None

    def reset(self):
        with self._buffer_lock:
            self._reset_state()
