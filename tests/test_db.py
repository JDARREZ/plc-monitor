import tempfile
import unittest
from pathlib import Path

from src.database.db_manager import DatabaseManager
from src.utils.config import ConfigManager


class TestDatabaseManager(unittest.TestCase):
    def test_create_insert_and_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "readings.db")
            db = DatabaseManager(db_path)
            db.insert_readings({"Tag1": "10", "Tag2": "20"}, "2026-01-01T10:00:00")
            rows = db.query_readings("2026-01-01T00:00:00", "2026-01-02T00:00:00")
            self.assertEqual(len(rows), 2)
            self.assertEqual({row[1] for row in rows}, {"Tag1", "Tag2"})

    def test_list_tags(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db_path = str(Path(tmp) / "readings.db")
            db = DatabaseManager(db_path)
            db.insert_readings({"B": 1, "A": 2}, "2026-01-01T10:00:00")
            self.assertEqual(db.list_tags(), ["A", "B"])


class TestConfigManager(unittest.TestCase):
    def test_save_and_load_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_path = str(Path(tmp) / "config.json")
            mgr = ConfigManager(config_path)
            mgr.save({"ip": "192.168.1.10", "slot": 1, "polling_ms": 500})
            loaded = mgr.load()
            self.assertEqual(loaded["ip"], "192.168.1.10")
            self.assertEqual(loaded["slot"], 1)
            self.assertEqual(loaded["polling_ms"], 500)


if __name__ == "__main__":
    unittest.main()
