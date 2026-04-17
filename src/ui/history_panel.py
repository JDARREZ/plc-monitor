from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Tuple

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.utils.exporter import export_readings_to_csv


class HistoryPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._rows: List[Tuple[int, str, str, str]] = []

        self.start_dt = QDateTimeEdit()
        self.end_dt = QDateTimeEdit()
        self.start_dt.setCalendarPopup(True)
        self.end_dt.setCalendarPopup(True)
        now = datetime.now()
        self.start_dt.setDateTime(QDateTime((now - timedelta(hours=1))))
        self.end_dt.setDateTime(QDateTime(now))

        self.tag_filter = QComboBox()
        self.tag_filter.addItem("Todos")

        self.query_btn = QPushButton("Consultar")
        self.export_btn = QPushButton("Exportar CSV")
        self.export_btn.clicked.connect(self._export)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Tag", "Valor", "Timestamp"])
        self.table.horizontalHeader().setStretchLastSection(True)

        filters = QHBoxLayout()
        filters.addWidget(self.start_dt)
        filters.addWidget(self.end_dt)
        filters.addWidget(self.tag_filter)
        filters.addWidget(self.query_btn)
        filters.addWidget(self.export_btn)

        root = QVBoxLayout()
        root.addLayout(filters)
        root.addWidget(self.table)
        self.setLayout(root)

    def get_filters(self) -> tuple[str, str, str]:
        start = self.start_dt.dateTime().toString("yyyy-MM-ddTHH:mm:ss")
        end = self.end_dt.dateTime().toString("yyyy-MM-ddTHH:mm:ss")
        return start, end, self.tag_filter.currentText()

    def set_available_tags(self, tags: List[str]) -> None:
        current = self.tag_filter.currentText()
        self.tag_filter.blockSignals(True)
        self.tag_filter.clear()
        self.tag_filter.addItem("Todos")
        for tag in tags:
            self.tag_filter.addItem(tag)
        idx = self.tag_filter.findText(current)
        if idx >= 0:
            self.tag_filter.setCurrentIndex(idx)
        self.tag_filter.blockSignals(False)

    def set_rows(self, rows: List[Tuple[int, str, str, str]]) -> None:
        self._rows = rows
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def _export(self) -> None:
        if not self._rows:
            QMessageBox.warning(self, "Historial", "No hay datos para exportar.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar CSV", "historial.csv", "CSV (*.csv)")
        if not file_path:
            return
        export_readings_to_csv(self._rows, file_path)
        QMessageBox.information(self, "Historial", "Exportación completada.")
