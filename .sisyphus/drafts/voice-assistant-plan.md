# Draft: Voice Activated Assistant Plan

## Project Overview
- **Goal**: Build a Python voice assistant using Qwen3-ASR + Qwen3-TTS
- **Platform**: Windows 11 + Python (GPU/CPU)
- **Current State**: Greenfield - only PRD.md exists

## Core Requirements (from PRD)

### 1. Audio Pipeline
- Microphone input with fixed frame size (20ms/32ms/50ms)
- VAD (Voice Activity Detection) for speech detection
- **Pause detection: 1 second silence = utterance end**
- Audio buffer only in memory (RAM), released after ASR

### 2. ASR (Automatic Speech Recognition)
- Qwen3-ASR for local/offline transcription
- Memory-only storage: `history_max_turns` (default 20)
- Merge short utterances if gap < 0.4s

### 3. Rule Engine
- JSON-based keyword matching
- Support: contains / regex / exact match modes
- Priority, cooldown, response templates
- TTS voice configuration

### 4. TTS (Text-to-Speech)
- Qwen3-TTS with streaming support
- Low first-packet latency
- Queue-based job processing

### 5. State Machine
- States: LISTENING → ASR_PROCESSING → SPEAKING → LISTENING
- **Critical**: ASR must pause during TTS playback
- Use threading.Event for synchronization

### 6. Memory & Privacy
- No disk storage by default
- Debug mode for wav/transcript output

## Technical Stack Questions
- Python package manager: pip / poetry / uv?
- Qwen3 models: Local or API?
- VAD library: Silero VAD or custom?

## Scope Decision Points
- GPU support: Required? (affects ASR/TTS performance)
- Debug mode: Include or skip for MVP?
- Hot reload JSON: Include or v2?

## Open Questions
1. Which VAD library to use? (Silero VAD recommended in PRD)
2. Audio device selection strategy?
3. Error handling approach for mic/ASR/TTS failures?
4. Log level preferences?
