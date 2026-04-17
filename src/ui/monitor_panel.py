from __future__ import annotations

from typing import Dict, List

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MonitorPanel(QWidget):
    discover_requested = pyqtSignal()
    selection_changed = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self._tags: List[Dict[str, str]] = []

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar tag...")
        self.search_input.textChanged.connect(self._apply_filter)

        discover_btn = QPushButton("Descubrir tags")
        apply_btn = QPushButton("Aplicar selección")
        discover_btn.clicked.connect(self.discover_requested.emit)
        apply_btn.clicked.connect(self._emit_selection)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Monitorear", "Tag", "Tipo", "Valor actual"])
        self.table.horizontalHeader().setStretchLastSection(True)

        top = QHBoxLayout()
        top.addWidget(self.search_input)
        top.addWidget(discover_btn)
        top.addWidget(apply_btn)

        root = QVBoxLayout()
        root.addLayout(top)
        root.addWidget(self.table)
        self.setLayout(root)

    def set_tags(self, tags: List[Dict[str, str]]) -> None:
        self._tags = tags
        self.table.setRowCount(len(tags))
        for row, tag in enumerate(tags):
            check = QTableWidgetItem()
            check.setFlags(check.flags() | Qt.ItemIsUserCheckable)
            check.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, check)
            self.table.setItem(row, 1, QTableWidgetItem(tag.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(tag.get("type", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(tag.get("value", "-"))))

    def _apply_filter(self, text: str) -> None:
        query = text.lower().strip()
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower() if self.table.item(row, 1) else ""
            self.table.setRowHidden(row, query not in name)

    def _emit_selection(self) -> None:
        selected = []
        for row in range(self.table.rowCount()):
            check = self.table.item(row, 0)
            name = self.table.item(row, 1)
            if check and name and check.checkState() == Qt.Checked:
                selected.append(name.text())
        self.selection_changed.emit(selected)

    def update_values(self, values: Dict[str, str]) -> None:
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            value_item = self.table.item(row, 3)
            if not name_item or not value_item:
                continue
            name = name_item.text()
            if name in values:
                value_item.setText(str(values[name]))
