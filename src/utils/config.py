from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


DEFAULT_CONFIG = {
    "ip": "",
    "slot": 0,
    "polling_ms": 1000,
}


class ConfigManager:
    def __init__(self, config_path: str = "~/.plc_monitor_config.json") -> None:
        self.config_path = Path(config_path).expanduser()

    def load(self) -> Dict:
        if not self.config_path.exists():
            return dict(DEFAULT_CONFIG)
        try:
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            return dict(DEFAULT_CONFIG)
        merged = dict(DEFAULT_CONFIG)
        merged.update({k: data.get(k, v) for k, v in DEFAULT_CONFIG.items()})
        return merged

    def save(self, config: Dict) -> None:
        payload = dict(DEFAULT_CONFIG)
        payload.update(config)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
