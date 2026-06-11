"""Виджет карточки пациента: поля + заглушка ассетов (ADR-012)."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from educase_core.domain.stages import PatientCard


class PatientCardWidget(QWidget):
    """Отображение карточки пациента: заголовок, строки «ключ: значение», ассеты-заглушка."""

    def __init__(self, card: PatientCard, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.card = card

        layout = QVBoxLayout(self)

        group = QGroupBox(card.title)
        group_layout = QVBoxLayout(group)

        for key, value in card.fields:
            row = QLabel(f"{key}: {value}")
            row.setWordWrap(True)
            group_layout.addWidget(row)

        if card.assets:
            asset_ids = ", ".join(card.assets)
            stub = QLabel(f"Материалы: {asset_ids}")  # TODO ADR-012 рендер ассетов
            stub.setEnabled(False)
            group_layout.addWidget(stub)

        layout.addWidget(group)
