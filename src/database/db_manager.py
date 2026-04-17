from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class DatabaseManager:
    def __init__(self, db_path: str = "plc_monitor.db") -> None:
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT NOT NULL,
                    value TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )

    def insert_readings(self, readings: Dict[str, str], timestamp: Optional[str] = None) -> None:
        if not readings:
            return
        ts = timestamp or datetime.now().isoformat(timespec="seconds")
        rows = [(name, str(value), ts) for name, value in readings.items()]
        with self._connect() as conn:
            conn.executemany("INSERT INTO readings (tag_name, value, timestamp) VALUES (?, ?, ?)", rows)

    def query_readings(self, start: str, end: str, tag_name: Optional[str] = None) -> List[Tuple[int, str, str, str]]:
        sql = "SELECT id, tag_name, value, timestamp FROM readings WHERE timestamp BETWEEN ? AND ?"
        params = [start, end]
        if tag_name and tag_name != "Todos":
            sql += " AND tag_name = ?"
            params.append(tag_name)
        sql += " ORDER BY timestamp DESC"
        with self._connect() as conn:
            return conn.execute(sql, params).fetchall()

    def list_tags(self) -> List[str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT DISTINCT tag_name FROM readings ORDER BY tag_name").fetchall()
        return [row[0] for row in rows]
