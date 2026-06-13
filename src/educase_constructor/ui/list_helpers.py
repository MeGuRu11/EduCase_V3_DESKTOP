"""Общие хелперы пустого состояния для списочных редакторов Constructor.

Подсказка-плейсхолдер показывается, пока список пуст, и скрывается, как только в нём
появляется хотя бы один элемент. Без QSS: приглушённый вид даёт ``setEnabled(False)``.
"""
from __future__ import annotations

from PySide6.QtWidgets import QLabel


def make_placeholder(text: str) -> QLabel:
    """Создать приглушённую подсказку пустого состояния (без стилевого слоя)."""
    label = QLabel(text)
    label.setEnabled(False)
    return label


def refresh_placeholder(placeholder: QLabel, is_empty: bool) -> None:
    """Показать подсказку, когда список пуст, и скрыть, когда в нём есть элементы."""
    placeholder.setVisible(is_empty)
