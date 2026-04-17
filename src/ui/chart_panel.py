from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChartPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.paused = False
        self.max_points = 300
        self.series: Dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=self.max_points))
        self.x_axis: Deque[int] = deque(maxlen=self.max_points)
        self.curves = {}

        self.plot = pg.PlotWidget()
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        self.plot.addLegend()
        self.plot.setMouseEnabled(x=True, y=True)

        self.pause_btn = QPushButton("Pausar")
        self.pause_btn.clicked.connect(self._toggle_pause)
        self.autoscroll = QCheckBox("Auto-scroll")
        self.autoscroll.setChecked(True)

        self.values_box = QTextEdit()
        self.values_box.setReadOnly(True)
        self.values_box.setMaximumHeight(90)

        top = QHBoxLayout()
        top.addWidget(self.pause_btn)
        top.addWidget(self.autoscroll)
        top.addStretch(1)

        root = QVBoxLayout()
        root.addLayout(top)
        root.addWidget(self.plot)
        root.addWidget(QLabel("Valores actuales:"))
        root.addWidget(self.values_box)
        self.setLayout(root)

    def _toggle_pause(self) -> None:
        self.paused = not self.paused
        self.pause_btn.setText("Reanudar" if self.paused else "Pausar")

    def set_tags(self, tags: List[str]) -> None:
        self.plot.clear()
        self.plot.addLegend()
        self.curves = {}
        for idx, tag in enumerate(tags):
            color = pg.intColor(idx, hues=max(1, len(tags)))
            self.curves[tag] = self.plot.plot(pen=pg.mkPen(color=color, width=2), name=tag)
            self.series[tag].clear()
        self.x_axis.clear()

    def add_reading(self, values: Dict[str, str]) -> None:
        if self.paused or not values:
            return
        next_x = self.x_axis[-1] + 1 if self.x_axis else 0
        self.x_axis.append(next_x)
        value_lines = []
        for tag, raw in values.items():
            try:
                num = float(raw)
            except (TypeError, ValueError):
                continue
            self.series[tag].append(num)
            if tag in self.curves:
                self.curves[tag].setData(list(self.x_axis)[-len(self.series[tag]):], list(self.series[tag]))
            value_lines.append(f"{tag}: {num}")
        self.values_box.setPlainText("\n".join(value_lines))
        if self.autoscroll.isChecked() and self.x_axis:
            self.plot.setXRange(max(0, self.x_axis[-1] - 50), self.x_axis[-1] + 5)
