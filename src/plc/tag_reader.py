from __future__ import annotations

from typing import Dict, List, Tuple

from src.plc.connection import PLCConnection


class TagReader:
    def __init__(self, connection: PLCConnection) -> None:
        self._connection = connection

    def poll(self, tags: List[str]) -> Tuple[bool, Dict[str, str], str]:
        return self._connection.read_tags(tags)
