"""Редакторы заданий по документам (Constructor): вариант, задание и список заданий.

Без визуальной полировки: только функциональные виджеты и layout-менеджеры. Публичные поля
ввода, списки вложенных редакторов и кнопки — точки доступа для тестов. Сборка значений в
драфты — через ``to_draft``; шаблон обманки отбрасывается на сборке (``template=None``).
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from educase_constructor.ui.template_editor import TemplateEditor
from educase_core.application.case_builder import (
    DocumentOptionDraft,
    DocumentTaskDraft,
)


class DocumentOptionEditor(QWidget):
    """Редактор варианта документа: заголовок, флаг верного выбора и встроенный шаблон.

    Шаблон заполняется только для верного варианта; для обманки сборка этапа ставит
    ``template=None`` независимо от содержимого редактора шаблона.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.title_edit = QLineEdit(self)
        self.correct_checkbox = QCheckBox("Верный документ", self)
        self.template_editor = TemplateEditor(self)

        title_form = QFormLayout()
        title_form.addRow("Название документа", self.title_edit)

        template_box = QGroupBox("Шаблон (для верного документа)")
        template_box_layout = QVBoxLayout(template_box)
        template_box_layout.addWidget(self.template_editor)

        layout = QVBoxLayout(self)
        layout.addLayout(title_form)
        layout.addWidget(self.correct_checkbox)
        layout.addWidget(template_box)

    def to_draft(self) -> DocumentOptionDraft:
        """Собрать ``DocumentOptionDraft`` из заголовка, флага и редактора шаблона."""
        return DocumentOptionDraft(
            title=self.title_edit.text(),
            is_correct=self.correct_checkbox.isChecked(),
            template=self.template_editor.to_draft(),
        )


class DocumentTaskEditor(QWidget):
    """Редактор задания по документу: формулировка + список редакторов вариантов."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.prompt_edit = QLineEdit(self)

        self.option_editors: list[DocumentOptionEditor] = []

        self.add_option_button = QPushButton("Добавить вариант", self)
        self.remove_option_button = QPushButton("Удалить последний", self)
        self.add_option_button.clicked.connect(self.add_option)
        self.remove_option_button.clicked.connect(self.remove_last_option)

        option_buttons = QHBoxLayout()
        option_buttons.addWidget(self.add_option_button)
        option_buttons.addWidget(self.remove_option_button)

        self._options_layout = QVBoxLayout()

        prompt_form = QFormLayout()
        prompt_form.addRow("Формулировка задания", self.prompt_edit)

        options_box = QGroupBox("Варианты документов")
        options_box_layout = QVBoxLayout(options_box)
        options_box_layout.addLayout(option_buttons)
        options_box_layout.addLayout(self._options_layout)

        layout = QVBoxLayout(self)
        layout.addLayout(prompt_form)
        layout.addWidget(options_box)

    def add_option(self) -> None:
        """Добавить редактор нового варианта документа в конец списка."""
        editor = DocumentOptionEditor(self)
        self.option_editors.append(editor)
        self._options_layout.addWidget(editor)

    def remove_last_option(self) -> None:
        """Удалить последний редактор варианта (если он есть)."""
        if not self.option_editors:
            return
        editor = self.option_editors.pop()
        self._options_layout.removeWidget(editor)
        editor.deleteLater()

    def to_draft(self) -> DocumentTaskDraft:
        """Собрать ``DocumentTaskDraft`` из формулировки и всех редакторов вариантов."""
        return DocumentTaskDraft(
            prompt=self.prompt_edit.text(),
            options=tuple(editor.to_draft() for editor in self.option_editors),
        )


class DocumentListEditor(QWidget):
    """Редактор списка заданий по документам этапа."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.task_editors: list[DocumentTaskEditor] = []

        self.add_task_button = QPushButton("Добавить задание", self)
        self.remove_task_button = QPushButton("Удалить последнее", self)
        self.add_task_button.clicked.connect(self.add_task)
        self.remove_task_button.clicked.connect(self.remove_last_task)

        task_buttons = QHBoxLayout()
        task_buttons.addWidget(self.add_task_button)
        task_buttons.addWidget(self.remove_task_button)

        self._tasks_layout = QVBoxLayout()

        layout = QVBoxLayout(self)
        layout.addLayout(task_buttons)
        layout.addLayout(self._tasks_layout)

    def add_task(self) -> None:
        """Добавить редактор нового задания в конец списка."""
        editor = DocumentTaskEditor(self)
        self.task_editors.append(editor)
        self._tasks_layout.addWidget(editor)

    def remove_last_task(self) -> None:
        """Удалить последний редактор задания (если он есть)."""
        if not self.task_editors:
            return
        editor = self.task_editors.pop()
        self._tasks_layout.removeWidget(editor)
        editor.deleteLater()

    def to_draft(self) -> tuple[DocumentTaskDraft, ...]:
        """Собрать драфты всех заданий по документам."""
        return tuple(editor.to_draft() for editor in self.task_editors)
