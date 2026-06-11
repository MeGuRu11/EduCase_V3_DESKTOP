"""Редактор шаблона документа (Constructor): заголовок + список полей.

Без визуальной полировки: только функциональные виджеты и layout-менеджеры. Публичные поля
ввода, список редакторов полей и кнопки — точки доступа для тестов. Сборка значений в драфт —
через ``to_draft``.
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from educase_constructor.ui.field_editor import FieldEditor
from educase_core.application.case_builder import TemplateDraft


class TemplateEditor(QWidget):
    """Редактор шаблона документа: заголовок + список редакторов полей."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.title_edit = QLineEdit(self)

        self.field_editors: list[FieldEditor] = []

        self.add_field_button = QPushButton("Добавить поле", self)
        self.remove_field_button = QPushButton("Удалить последнее", self)
        self.add_field_button.clicked.connect(self.add_field)
        self.remove_field_button.clicked.connect(self.remove_last_field)

        field_buttons = QHBoxLayout()
        field_buttons.addWidget(self.add_field_button)
        field_buttons.addWidget(self.remove_field_button)

        self._fields_layout = QVBoxLayout()

        title_form = QFormLayout()
        title_form.addRow("Заголовок шаблона", self.title_edit)

        fields_box = QGroupBox("Поля шаблона")
        fields_box_layout = QVBoxLayout(fields_box)
        fields_box_layout.addLayout(field_buttons)
        fields_box_layout.addLayout(self._fields_layout)

        layout = QVBoxLayout(self)
        layout.addLayout(title_form)
        layout.addWidget(fields_box)

    def add_field(self) -> None:
        """Добавить редактор нового поля в конец списка."""
        editor = FieldEditor(self)
        self.field_editors.append(editor)
        self._fields_layout.addWidget(editor)

    def remove_last_field(self) -> None:
        """Удалить последний редактор поля (если он есть)."""
        if not self.field_editors:
            return
        editor = self.field_editors.pop()
        self._fields_layout.removeWidget(editor)
        editor.deleteLater()

    def to_draft(self) -> TemplateDraft:
        """Собрать ``TemplateDraft`` из заголовка и всех редакторов полей."""
        return TemplateDraft(
            title=self.title_edit.text(),
            fields=tuple(editor.to_draft() for editor in self.field_editors),
        )
