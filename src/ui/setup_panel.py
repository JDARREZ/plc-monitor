from __future__ import annotations

from typing import Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SetupPanel(QWidget):
    connection_requested = pyqtSignal(str, int)
    config_saved = pyqtSignal(dict)

    def __init__(self, initial_config: Dict) -> None:
        super().__init__()
        self.ip_input = QLineEdit(initial_config.get("ip", ""))
        self.slot_input = QSpinBox()
        self.slot_input.setRange(0, 17)
        self.slot_input.setValue(int(initial_config.get("slot", 0)))
        self.polling_input = QSpinBox()
        self.polling_input.setRange(100, 60000)
        self.polling_input.setSingleStep(100)
        self.polling_input.setValue(int(initial_config.get("polling_ms", 1000)))

        test_btn = QPushButton("Probar conexión")
        save_btn = QPushButton("Guardar configuración")
        test_btn.clicked.connect(self._emit_connection_request)
        save_btn.clicked.connect(self._emit_save)

        form = QFormLayout()
        form.addRow("IP del PLC:", self.ip_input)
        form.addRow("Slot:", self.slot_input)
        form.addRow("Polling (ms):", self.polling_input)

        btns = QHBoxLayout()
        btns.addWidget(test_btn)
        btns.addWidget(save_btn)

        root = QVBoxLayout()
        root.addWidget(QLabel("Configura la conexión EtherNet/IP al PLC Allen Bradley."))
        root.addLayout(form)
        root.addLayout(btns)
        root.addStretch(1)
        self.setLayout(root)

    def _emit_connection_request(self) -> None:
        self.connection_requested.emit(self.ip_input.text().strip(), self.slot_input.value())

    def _emit_save(self) -> None:
        payload = self.get_config()
        self.config_saved.emit(payload)
        QMessageBox.information(self, "Configuración", "Configuración guardada correctamente.")

    def get_config(self) -> Dict:
        return {
            "ip": self.ip_input.text().strip(),
            "slot": self.slot_input.value(),
            "polling_ms": self.polling_input.value(),
        }
