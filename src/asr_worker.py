"""ASR Worker module - Qwen3-ASR integration"""

import threading
import queue
import time
from typing import Optional, Callable
from dataclasses import dataclass
import numpy as np


@dataclass
class ASRResult:
    transcript: str
    language: Optional[str] = None
    confidence: float = 0.0
    duration_ms: int = 0


class ASRWorker:
    def __init__(
        self,
        model_path: Optional[str] = None,
        on_result: Optional[Callable[[ASRResult], None]] = None,
    ):
        self.model_path = model_path
        self.on_result = on_result

        self._input_queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._is_running = False

        self._model = None
        self._model_loaded = False

    def load_model(self):
        pass

    def start(self):
        if self._is_running:
            return

        self._is_running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def stop(self):
        self._is_running = False

        if self._worker_thread:
            self._input_queue.put(None)
            self._worker_thread.join(timeout=2.0)
            self._worker_thread = None

    def process(self, audio: np.ndarray) -> bool:
        if not self._is_running:
            return False

        self._input_queue.put(audio)
        return True

    def _worker_loop(self):
        while self._is_running:
            try:
                audio = self._input_queue.get(timeout=0.1)

                if audio is None:
                    break

                result = self._recognize(audio)

                if result and self.on_result:
                    self.on_result(result)

                self._input_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"[ASR] Error: {e}")

    def _recognize(self, audio: np.ndarray) -> Optional[ASRResult]:
        if not self._model_loaded:
            return ASRResult(transcript="[ASR model not loaded]")

        return None
