"""Тесты AssetPicker: стабильный id-ссылка на файл без дёрганья ``QFileDialog``."""
from __future__ import annotations

from pathlib import Path

from pytestqt.qtbot import QtBot

from educase_constructor.ui.asset_picker import AssetPicker


def test_value_none_by_default(qtbot: QtBot) -> None:
    """До выбора файла ``value()`` равен ``None``."""
    picker = AssetPicker()
    qtbot.addWidget(picker)
    assert picker.value() is None


def test_set_file_builds_ref(qtbot: QtBot, tmp_path: Path) -> None:
    """``set_file`` даёт ``AssetRef``: непустой id, путь и имя файла сохранены."""
    picker = AssetPicker()
    qtbot.addWidget(picker)

    source = tmp_path / "scheme.png"
    source.write_bytes(b"PNG")
    picker.set_file(str(source))

    ref = picker.value()
    assert ref is not None
    assert ref.asset_id  # непустой стабильный id
    assert ref.asset_id.endswith(".png")  # расширение исходного файла сохранено
    assert ref.source_path == str(source)
    assert ref.display_name == "scheme.png"


def test_clear_resets_value(qtbot: QtBot, tmp_path: Path) -> None:
    """``clear()`` сбрасывает ссылку обратно в ``None``."""
    picker = AssetPicker()
    qtbot.addWidget(picker)

    source = tmp_path / "scheme.jpg"
    source.write_bytes(b"JPG")
    picker.set_file(str(source))
    assert picker.value() is not None

    picker.clear()
    assert picker.value() is None
