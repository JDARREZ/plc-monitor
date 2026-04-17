from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from src.database.db_manager import DatabaseManager
from src.plc.connection import PLCConnection
from src.plc.tag_reader import TagReader
from src.ui.chart_panel import ChartPanel
from src.ui.history_panel import HistoryPanel
from src.ui.monitor_panel import MonitorPanel
from src.ui.setup_panel import SetupPanel
from src.ui.styles import DARK_STYLE
from src.utils.config import ConfigManager


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PLC Monitor - Allen Bradley")
        self.resize(1200, 760)
        self.setStyleSheet(DARK_STYLE)

        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.load()
        self.db = DatabaseManager(str(Path.home() / "plc_monitor" / "plc_monitor.db"))
        self.connection = PLCConnection()
        self.tag_reader = TagReader(self.connection)

        self.selected_tags: list[str] = []
        self.connected = False

        self.setup_panel = SetupPanel(self.config)
        self.monitor_panel = MonitorPanel()
        self.chart_panel = ChartPanel()
        self.history_panel = HistoryPanel()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.setup_panel, "Setup")
        self.tabs.addTab(self.monitor_panel, "Monitor")
        self.tabs.addTab(self.chart_panel, "Gráficas")
        self.tabs.addTab(self.history_panel, "Historial")
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self._poll_tags)
        self._apply_polling_interval(self.config.get("polling_ms", 1000))

        self._connect_signals()
        self._refresh_status("Listo")
        self._refresh_history_tags()

    def _connect_signals(self) -> None:
        self.setup_panel.connection_requested.connect(self._test_connection)
        self.setup_panel.config_saved.connect(self._save_config)
        self.monitor_panel.discover_requested.connect(self._discover_tags)
        self.monitor_panel.selection_changed.connect(self._set_selected_tags)
        self.history_panel.query_btn.clicked.connect(self._query_history)

    def _save_config(self, payload: dict) -> None:
        self.config = payload
        self.config_mgr.save(payload)
        self._apply_polling_interval(payload.get("polling_ms", 1000))
        self._refresh_status("Configuración guardada")

    def _apply_polling_interval(self, polling_ms: int) -> None:
        self.poll_timer.setInterval(max(100, int(polling_ms)))
        if not self.poll_timer.isActive():
            self.poll_timer.start()

    def _test_connection(self, ip: str, slot: int) -> None:
        ok, msg = self.connection.test_connection(ip, slot)
        self.connected = ok
        if ok:
            self.config["ip"] = ip
            self.config["slot"] = slot
        QMessageBox.information(self, "Conexión PLC", msg)
        self._refresh_status(msg)

    def _discover_tags(self) -> None:
        ok, tags, msg = self.connection.discover_tags()
        if not ok:
            QMessageBox.warning(self, "Descubrir Tags", msg)
            self._refresh_status(msg)
            return
        self.monitor_panel.set_tags(tags)
        self._refresh_status(f"{len(tags)} tags descubiertos")

    def _set_selected_tags(self, tags: list[str]) -> None:
        self.selected_tags = tags
        self.chart_panel.set_tags(tags)
        self._refresh_status("Tags monitoreados actualizados")

    def _poll_tags(self) -> None:
        if not self.connected or not self.selected_tags:
            return
        ok, values, msg = self.tag_reader.poll(self.selected_tags)
        if not ok:
            self._refresh_status(msg)
            return
        if values:
            ts = datetime.now().isoformat(timespec="seconds")
            self.monitor_panel.update_values(values)
            self.chart_panel.add_reading(values)
            self.db.insert_readings(values, ts)
            self._refresh_history_tags()
            self._refresh_status("Lectura en tiempo real")

    def _query_history(self) -> None:
        start, end, tag = self.history_panel.get_filters()
        rows = self.db.query_readings(start, end, tag)
        self.history_panel.set_rows(rows)
        self._refresh_status(f"Consulta historial: {len(rows)} registros")

    def _refresh_history_tags(self) -> None:
        self.history_panel.set_available_tags(self.db.list_tags())

    def _refresh_status(self, message: str) -> None:
        ip = self.config.get("ip", "-") or "-"
        status = "Conectado" if self.connected else "Desconectado"
        self.status.showMessage(
            f"{message} | Estado: {status} | IP: {ip} | Tags monitoreados: {len(self.selected_tags)}"
        )
