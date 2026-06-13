"""Виджет выбора файла-ассета (Constructor): Проводник → стабильный id-ссылка.

Вариант B: ``asset_id`` стабилен (``uuid4`` + исходное расширение), исходное имя файла
хранится только для показа. Без визуальной полировки: только функциональные виджеты и
layout-менеджеры. Кнопка «Обзор…» открывает ``QFileDialog``; тестируемый шов ``set_file``
делает ту же работу без диалога. Значение собирается через ``value`` (``AssetRef`` или ``None``).
"""
from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from educase_core.application.case_builder import AssetRef

_PLACEHOLDER = "файл не выбран"
_IMAGE_FILTER = "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"


class AssetPicker(QWidget):
    """Выбор файла-ассета: метка имени + кнопки «Обзор…»/«Очистить»; стабильный id-ссылка."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._ref: AssetRef | None = None

        self.name_label = QLabel(_PLACEHOLDER, self)
        self.browse_button = QPushButton("Обзор…", self)
        self.clear_button = QPushButton("Очистить", self)
        self.browse_button.clicked.connect(self._browse)
        self.clear_button.clicked.connect(self.clear)

        layout = QHBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.clear_button)

    def _browse(self) -> None:
        """Открыть Проводник и, если файл выбран, передать путь в ``set_file``."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", _IMAGE_FILTER
        )
        if path:
            self.set_file(path)

    def set_file(self, path: str) -> None:
        """Зафиксировать выбранный файл: сгенерировать стабильный id, обновить метку.

        Тестируемый шов: делает то же, что колбэк диалога, но без ``QFileDialog``.
        ``asset_id`` — ``uuid4`` + исходное расширение; имя файла хранится лишь для показа.
        """
        source = Path(path)
        asset_id = f"{uuid4().hex}{source.suffix}"
        self._ref = AssetRef(
            asset_id=asset_id, source_path=path, display_name=source.name
        )
        self.name_label.setText(source.name)

    def clear(self) -> None:
        """Сбросить выбор: ссылка → ``None``, метка → плейсхолдер."""
        self._ref = None
        self.name_label.setText(_PLACEHOLDER)

    def value(self) -> AssetRef | None:
        """Вернуть ``AssetRef`` выбранного файла или ``None``, если файл не выбран."""
        return self._ref
