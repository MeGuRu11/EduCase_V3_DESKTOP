from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(autouse=True)
def _isolated_data_dir(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Изолируем каталог данных, чтобы тесты не писали в %LOCALAPPDATA%."""
    monkeypatch.setenv("EDUCASE_DATA_DIR", str(tmp_path))