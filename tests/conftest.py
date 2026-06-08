"""Общие фикстуры. pytest-qt предоставляет qtbot/qapp автоматически."""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolated_data_dir(tmp_path, monkeypatch):
    """Изолируем каталог данных, чтобы тесты не писали в %LOCALAPPDATA%."""
    monkeypatch.setenv("EDUCASE_DATA_DIR", str(tmp_path))
