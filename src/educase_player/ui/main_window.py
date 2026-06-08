"""Главное окно Player (каркас)."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EduCase Player")
        self.resize(1000, 700)

        central = QWidget(self)
        layout = QVBoxLayout(central)
        label = QLabel("EduCase Player — каркас.\nЗагрузите кейс (.educase).", central)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setCentralWidget(central)
