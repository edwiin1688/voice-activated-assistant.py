"""Orchestrator module - State machine and thread coordination"""

import threading
import time
from enum import Enum
from typing import Optional, Callable
from dataclasses import dataclass

from .audio_input import AudioInput, AudioConfig
from .vad_segmenter import VADSegmenter, VADConfig, Utterance
from .asr_worker import ASRWorker, ASRResult
from .rule_engine import RuleEngine, TTSJob
from .tts_worker import TTSWorker


class State(Enum):
    LISTENING = "LISTENING"
    ASR_PROCESSING = "ASR_PROCESSING"
    SPEAKING = "SPEAKING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


@dataclass
class OrchestratorConfig:
    sample_rate: int = 16000
    frame_duration_ms: int = 30
    silence_threshold: float = 0.5
    silence_duration: float = 1.0
    min_utterance_ms: int = 300
    max_utterance_s: int = 15
    resume_grace_s: float = 0.2
    rules_path: str = "config/rules.json"
    debug: bool = False
    audio_device: Optional[int] = None
    mock_mode: bool = False


class Orchestrator:
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        self.config = config or OrchestratorConfig()

        self._state = State.STOPPED
        self._state_lock = threading.Lock()

        self._audio_input = AudioInput(
            config=AudioConfig(
                sample_rate=self.config.sample_rate,
                frame_duration_ms=self.config.frame_duration_ms,
                device=self.config.audio_device,
            ),
            callback=self._on_audio_frame,
        )

        self._vad = VADSegmenter(
            config=VADConfig(
                silence_threshold=self.config.silence_threshold,
                min_silence_duration=self.config.silence_duration,
                min_utterance_ms=self.config.min_utterance_ms,
                max_utterance_s=self.config.max_utterance_s,
                sample_rate=self.config.sample_rate,
            ),
            on_utterance=self._on_utterance,
        )

        self._asr = ASRWorker(on_result=self._on_asr_result)
        self._rule_engine = RuleEngine(rules_path=self.config.rules_path)
        self._tts = TTSWorker(on_complete=self._on_tts_complete)

        self._speaking_event = self._tts.speaking_event

        self._is_running = False

    @property
    def state(self) -> State:
        with self._state_lock:
            return self._state

    def set_state(self, new_state: State):
        with self._state_lock:
            self._state = new_state

    def start(self) -> bool:
        if self._is_running:
            return False

        print("[ORCHESTRATOR] Loading rules...")
        self._rule_engine.load_rules()
        print("[ORCHESTRATOR] Loading VAD...")
        self._vad.load_vad()

        print("[ORCHESTRATOR] Starting ASR...")
        self._asr.load_model()
        self._asr.start()

        print("[ORCHESTRATOR] Starting TTS...")
        self._tts.load_model()
        self._tts.start()
        print("[ORCHESTRATOR] All threads started")

        if self.config.mock_mode:
            print("[ORCHESTRATOR] Running in MOCK mode - no audio input required")
            self.set_state(State.LISTENING)
            self._is_running = True
            print("[STATE] -> LISTENING (waiting for speech...)")
            return True

        if not self._audio_input.start():
            print("[ORCHESTRATOR] Failed to start audio input")
            return False

        self.set_state(State.LISTENING)
        print("[STATE] -> LISTENING (waiting for speech...)")
        self._is_running = True
        return True

    def stop(self):
        if not self._is_running:
            return

        self._audio_input.stop()
        self._asr.stop()
        self._tts.stop()

        self.set_state(State.STOPPED)
        self._is_running = False

    def _on_audio_frame(self, audio):
        if self._speaking_event.is_set():
            return

        if self.state == State.SPEAKING:
            return

        is_speech = self._vad.process_frame(audio)

    def _on_utterance(self, utterance: Utterance):
        print(f"[VAD] Utterance detected: {utterance.duration_ms}ms")
        self.set_state(State.ASR_PROCESSING)

        self._asr.process(utterance.audio)

    def _on_asr_result(self, result: ASRResult):
        transcript = result.transcript.strip()

        print(f"[ASR] Result: {transcript!r}")

        if not transcript:
            print("[STATE] -> LISTENING (empty transcript)")
            self.set_state(State.LISTENING)
            return

        if self._speaking_event.is_set():
            print("[STATE] -> LISTENING (TTS speaking)")
            self.set_state(State.LISTENING)
            return

        job = self._rule_engine.match(transcript)

        if job:
            print(f"┌─────────────────────────────────┐")
            print(f"│ 🎯 觸發規則: {job.rule_id:<20} │")
            print(f"│ 📝 辨識文字: {transcript:<20} │")
            print(f"│ 🔊 朗讀內容: {job.text[:20]:<20} │")
            print(f"└─────────────────────────────────┘")
            success = self._tts.speak(job)
            if success:
                self.set_state(State.SPEAKING)
            else:
                print("[STATE] -> LISTENING (TTS queue full)")
                self.set_state(State.LISTENING)
        else:
            print(f"[RULE] No match for: {transcript!r}")
            print("[STATE] -> LISTENING")
            self.set_state(State.LISTENING)

    def _on_tts_complete(self, result):
        print(f"[TTS] Finished: {result.duration_ms}ms")
        time.sleep(self.config.resume_grace_s)
        print("[STATE] -> LISTENING (waiting for speech...)")
        self.set_state(State.LISTENING)

    def simulate_utterance(self, text: str):
        print(f"[MOCK] Simulating utterance: {text}")
        result = ASRResult(transcript=text)
        self._on_asr_result(result)
