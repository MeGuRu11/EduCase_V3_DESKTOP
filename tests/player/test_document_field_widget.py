"""Тесты DocumentFieldWidget: тип виджета по FieldType и делегирование проверки в домен."""
from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QLineEdit
from pytestqt.qtbot import QtBot

from educase_core.domain.documents import (
    ChoiceMatch,
    DateMatch,
    DocumentField,
    FieldType,
    NumberMatch,
    TextMatch,
)
from educase_core.domain.search import SynonymSet
from educase_player.ui.document_field_widget import DocumentFieldWidget


def test_text_field_gives_line_edit(qtbot: QtBot) -> None:
    """TEXT-поле → QLineEdit."""
    field = DocumentField(
        id="f1",
        type=FieldType.TEXT,
        rule=TextMatch(keywords=SynonymSet(canonical="да")),
        label="Метка",
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QLineEdit)


def test_number_field_gives_line_edit(qtbot: QtBot) -> None:
    """NUMBER-поле → QLineEdit."""
    field = DocumentField(
        id="f2",
        type=FieldType.NUMBER,
        rule=NumberMatch(value=42.0),
        label="Число",
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QLineEdit)


def test_date_field_gives_line_edit(qtbot: QtBot) -> None:
    """DATE-поле → QLineEdit."""
    field = DocumentField(
        id="f3",
        type=FieldType.DATE,
        rule=DateMatch(value="2026-01-01"),
        label="Дата",
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QLineEdit)


def test_choice_field_gives_combo_with_placeholder_and_options(qtbot: QtBot) -> None:
    """CHOICE-поле → QComboBox: плейсхолдер + все опции поля."""
    field = DocumentField(
        id="f4",
        type=FieldType.CHOICE,
        rule=ChoiceMatch(correct=("Вариант А",)),
        label="Выбор",
        options=("Вариант А", "Вариант Б"),
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QComboBox)
    assert w.input.count() == 3  # плейсхолдер + 2 опции
    assert w.input.itemText(0) == "— выберите —"
    assert w.input.itemText(1) == "Вариант А"
    assert w.input.itemText(2) == "Вариант Б"


def test_check_correct_text_answer(qtbot: QtBot) -> None:
    """check() → True для правильного текстового ответа."""
    field = DocumentField(
        id="f5",
        type=FieldType.TEXT,
        rule=TextMatch(keywords=SynonymSet(canonical="сальмонеллёз")),
        label="Диагноз",
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QLineEdit)
    w.input.setText("сальмонеллёз")
    assert w.check() is True


def test_check_incorrect_text_answer(qtbot: QtBot) -> None:
    """check() → False для неправильного текстового ответа."""
    field = DocumentField(
        id="f6",
        type=FieldType.TEXT,
        rule=TextMatch(keywords=SynonymSet(canonical="сальмонеллёз")),
        label="Диагноз",
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QLineEdit)
    w.input.setText("тиф")
    assert w.check() is False


def test_choice_answer_empty_for_placeholder(qtbot: QtBot) -> None:
    """answer() для CHOICE с плейсхолдером (index 0) → пустая строка."""
    field = DocumentField(
        id="f7",
        type=FieldType.CHOICE,
        rule=ChoiceMatch(correct=("Вариант А",)),
        label="Выбор",
        options=("Вариант А",),
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QComboBox)
    assert w.input.currentIndex() == 0
    assert w.answer() == ""


def test_choice_answer_returns_selected_text(qtbot: QtBot) -> None:
    """answer() для CHOICE → текст выбранного элемента."""
    field = DocumentField(
        id="f8",
        type=FieldType.CHOICE,
        rule=ChoiceMatch(correct=("Вариант А",)),
        label="Выбор",
        options=("Вариант А", "Вариант Б"),
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QComboBox)
    w.input.setCurrentIndex(1)
    assert w.answer() == "Вариант А"


def test_check_delegates_to_domain_choice(qtbot: QtBot) -> None:
    """check() делегирует в DocumentField.check без своей логики правильности."""
    field = DocumentField(
        id="f9",
        type=FieldType.CHOICE,
        rule=ChoiceMatch(correct=("Да",)),
        label="Да/Нет",
        options=("Да", "Нет"),
    )
    w = DocumentFieldWidget(field)
    qtbot.addWidget(w)
    assert isinstance(w.input, QComboBox)
    w.input.setCurrentIndex(1)  # "Да"
    assert w.check() is True
    w.input.setCurrentIndex(2)  # "Нет"
    assert w.check() is False
