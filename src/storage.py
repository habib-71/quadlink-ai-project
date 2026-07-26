"""Small, fault-tolerant runtime persistence for QuadLink preferences and totals."""

import json
import os

from config import DATA_DIR, STATE_FILE


class RuntimeStorage:
    def load(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as state_file:
                data = json.load(state_file)
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def save(self, settings, stats):
        payload = {"settings": settings, "statistics": stats}
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as state_file:
                json.dump(payload, state_file, indent=2)
        except OSError:
            # The game remains usable even in read-only installation locations.
            pass
