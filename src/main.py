"""Main entry point for Voice Activated Assistant"""

import sys
import signal
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.orchestrator import Orchestrator, OrchestratorConfig
from src.logging_config import setup_logging
from src.audio_input import AudioInput, AudioConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Voice Activated Assistant")
    parser.add_argument(
        "--config", type=str, default="config/config.yaml", help="Path to config file"
    )
    parser.add_argument(
        "--rules", type=str, default="config/rules.json", help="Path to rules JSON file"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--list-devices", action="store_true", help="List available audio devices"
    )
    parser.add_argument("--device", type=int, default=None, help="Audio device index")
    parser.add_argument(
        "--mock-mode", action="store_true", help="Run without microphone for testing"
    )
    parser.add_argument(
        "--test", type=str, help="Test with a specific phrase (implies --mock-mode)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list_devices:
        audio = AudioInput()
        audio.list_devices()
        return

    logger = setup_logging(debug=args.debug)

    config = OrchestratorConfig(
        rules_path=args.rules,
        debug=args.debug,
        audio_device=args.device,
        mock_mode=args.mock_mode or args.test is not None,
    )

    orchestrator = Orchestrator(config)

    def signal_handler(sig, frame):
        print("\nShutting down...")
        orchestrator.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting Voice Activated Assistant...")
    print(f"Rules file: {args.rules}")
    if config.mock_mode:
        print("Mode: MOCK (no audio input)")
    elif args.device is not None:
        print(f"Using audio device: {args.device}")
    print("Press Ctrl+C to stop")

    success = orchestrator.start()

    if not success:
        print("\nFailed to start audio. Use --list-devices to see available devices")
        print("Example: python src/main.py --rules config/rules.json --device 0")
        print("Or use --mock-mode for testing without microphone")
        sys.exit(1)

    if args.test:
        print(f"\n[Test] Simulating: '{args.test}'")
        orchestrator.simulate_utterance(args.test)

    while True:
        try:
            signal.pause()
        except AttributeError:
            import time

            time.sleep(1)


if __name__ == "__main__":
    main()
