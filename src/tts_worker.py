"""TTS Worker module - Text-to-Speech using espeak-ng"""

import threading
import queue
import time
import subprocess
from typing import Optional, Callable
from dataclasses import dataclass
from .rule_engine import TTSJob


@dataclass
class TTSResult:
    job_id: str
    success: bool
    duration_ms: int = 0
    error: Optional[str] = None


class TTSWorker:
    def __init__(
        self,
        model_path: Optional[str] = None,
        on_complete: Optional[Callable[[TTSResult], None]] = None,
    ):
        self.model_path = model_path
        self.on_complete = on_complete

        self._job_queue: queue.Queue = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._is_speaking = False

        self._max_queue_size = 10

        self._speaking_event = threading.Event()

    @property
    def is_speaking(self) -> bool:
        return self._is_speaking

    @property
    def speaking_event(self) -> threading.Event:
        return self._speaking_event

    def load_model(self):
        print("[TTS] Using espeak-ng for speech synthesis")

    def start(self):
        if self._is_running:
            return

        self._is_running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def stop(self):
        self._is_running = False

        if self._worker_thread:
            self._job_queue.put(None)
            self._worker_thread.join(timeout=2.0)
            self._worker_thread = None

    def speak(self, job: TTSJob) -> bool:
        if self._job_queue.qsize() >= self._max_queue_size:
            return False

        self._job_queue.put(job)
        return True

    def _worker_loop(self):
        while self._is_running:
            try:
                job = self._job_queue.get(timeout=0.1)

                if job is None:
                    break

                self._speak(job)

                self._job_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"[TTS] Error: {e}")

    def _speak(self, job: TTSJob):
        self._is_speaking = True
        self._speaking_event.set()

        start_time = time.time()

        try:
            subprocess.run(
                ["espeak-ng", "-v", "zh", "-s", "140", job.text],
                capture_output=True,
                timeout=10,
            )
        except FileNotFoundError:
            print("[TTS] espeak not found, skipping audio output")
        except Exception as e:
            print(f"[TTS] Speak error: {e}")

        duration_ms = int((time.time() - start_time) * 1000)

        result = TTSResult(job_id=job.rule_id, success=True, duration_ms=duration_ms)

        if self.on_complete:
            self.on_complete(result)

        self._is_speaking = False
        self._speaking_event.clear()
