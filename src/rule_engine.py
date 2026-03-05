"""Rule Engine module - JSON-based keyword matching"""

import re
import json
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Rule:
    id: str
    keywords: List[str]
    match_mode: str = "contains"
    priority: int = 100
    cooldown_s: float = 0.0
    response_type: str = "speak_text"
    text_template: Optional[str] = None
    kv: Optional[Dict[str, str]] = None
    tts_voice: Optional[str] = None
    tts_language: Optional[str] = None


@dataclass
class TTSJob:
    rule_id: str
    text: str
    voice: Optional[str] = None
    language: Optional[str] = None


class RuleEngine:
    def __init__(self, rules_path: Optional[str] = None):
        self.rules_path = rules_path
        self._rules: List[Rule] = []
        self._last_triggered: Dict[str, float] = {}
        self._history: List[str] = []
        self._history_max = 20
        self._rules_mtime: Optional[float] = None

    def load_rules(self, path: Optional[str] = None):
        path = path or self.rules_path
        if not path:
            return

        file_path = Path(path)
        if not file_path.exists():
            return

        self._rules_mtime = file_path.stat().st_mtime

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._rules = []
        for item in data.get("rules", []):
            rule = Rule(
                id=item.get("id", ""),
                keywords=item.get("keywords", []),
                match_mode=item.get("match_mode", "contains"),
                priority=item.get("priority", 100),
                cooldown_s=item.get("cooldown_s", 0.0),
                response_type=item.get("response", {}).get("type", "speak_text"),
                text_template=item.get("response", {}).get("text_template"),
                kv=item.get("response", {}).get("kv"),
                tts_voice=item.get("tts", {}).get("voice"),
                tts_language=item.get("tts", {}).get("language"),
            )
            self._rules.append(rule)

        self._rules.sort(key=lambda r: r.priority)

    def check_hot_reload(self):
        if not self.rules_path:
            return False

        path = Path(self.rules_path)
        if not path.exists():
            return False

        current_mtime = path.stat().st_mtime

        if self._rules_mtime and current_mtime > self._rules_mtime:
            self.load_rules()
            return True

        return False

    def match(self, transcript: str) -> Optional[TTSJob]:
        self.check_hot_reload()

        self._history.append(transcript)
        if len(self._history) > self._history_max:
            self._history.pop(0)

        current_time = time.time()
        matched_rules = []

        for rule in self._rules:
            if not self._check_keywords(transcript, rule):
                continue

            if rule.cooldown_s > 0:
                last_time = self._last_triggered.get(rule.id, 0)
                if current_time - last_time < rule.cooldown_s:
                    continue

            matched_rules.append(rule)

        if not matched_rules:
            return None

        rule = matched_rules[0]
        self._last_triggered[rule.id] = current_time

        text = self._generate_response(rule, transcript)

        return TTSJob(
            rule_id=rule.id, text=text, voice=rule.tts_voice, language=rule.tts_language
        )

    def _check_keywords(self, transcript: str, rule: Rule) -> bool:
        transcript_lower = transcript.lower()

        for keyword in rule.keywords:
            keyword_lower = keyword.lower()

            if rule.match_mode == "contains":
                if keyword_lower in transcript_lower:
                    return True

            elif rule.match_mode == "exact":
                if keyword_lower == transcript_lower:
                    return True

            elif rule.match_mode == "regex":
                try:
                    if re.search(keyword, transcript, re.IGNORECASE):
                        return True
                except re.error:
                    pass

        return False

    def _generate_response(self, rule: Rule, transcript: str) -> str:
        if rule.response_type == "speak_text" and rule.text_template:
            return rule.text_template

        if rule.response_type == "speak_kv" and rule.kv:
            parts = []
            for key, value in rule.kv.items():
                parts.append(f"{key}: {value}")
            return ", ".join(parts)

        return transcript

    def get_history(self) -> List[str]:
        return self._history.copy()
