"""Редактор одной карточки пациента (Constructor, этап «Пациенты»).

Без визуальной полировки: только функциональные виджеты и layout-менеджеры. Публичные поля
ввода и кнопки — точки доступа для тестов. Сборка значений в домен — через ``to_draft``.
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from educase_core.application.case_builder import PatientDraft


class PatientEditor(QWidget):
    """Редактор карточки пациента: id, заголовок, таблица «поле/значение», строка ассетов."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.id_edit = QLineEdit(self)
        self.title_edit = QLineEdit(self)
        self.assets_edit = QLineEdit(self)

        self.fields_table = QTableWidget(0, 2, self)
        self.fields_table.setHorizontalHeaderLabels(["Поле", "Значение"])

        self.add_row_button = QPushButton("+ строка", self)
        self.remove_row_button = QPushButton("− строка", self)
        self.add_row_button.clicked.connect(self.add_field_row)
        self.remove_row_button.clicked.connect(self.remove_last_field_row)

        form = QFormLayout()
        form.addRow("Идентификатор", self.id_edit)
        form.addRow("Заголовок", self.title_edit)
        form.addRow("Ассеты (id через запятую)", self.assets_edit)

        row_buttons = QHBoxLayout()
        row_buttons.addWidget(self.add_row_button)
        row_buttons.addWidget(self.remove_row_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.fields_table)
        layout.addLayout(row_buttons)

    def add_field_row(self) -> None:
        """Добавить пустую строку «поле/значение»."""
        self.fields_table.insertRow(self.fields_table.rowCount())

    def remove_last_field_row(self) -> None:
        """Удалить последнюю строку таблицы полей (если она есть)."""
        count = self.fields_table.rowCount()
        if count:
            self.fields_table.removeRow(count - 1)

    def _collect_fields(self) -> tuple[tuple[str, str], ...]:
        rows: list[tuple[str, str]] = []
        for row in range(self.fields_table.rowCount()):
            key_item = self.fields_table.item(row, 0)
            value_item = self.fields_table.item(row, 1)
            key = key_item.text() if key_item is not None else ""
            value = value_item.text() if value_item is not None else ""
            rows.append((key, value))
        return tuple(rows)

    def _collect_assets(self) -> tuple[str, ...]:
        parts = (chunk.strip() for chunk in self.assets_edit.text().split(","))
        return tuple(part for part in parts if part)

    def to_draft(self) -> PatientDraft:
        """Собрать ``PatientDraft`` из текущих значений виджетов."""
        return PatientDraft(
            id=self.id_edit.text(),
            title=self.title_edit.text(),
            fields=self._collect_fields(),
            assets=self._collect_assets(),
        )
