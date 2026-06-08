"""Дымовые тесты: пакеты импортируются, версия доступна."""
from __future__ import annotations

import educase_core
from educase_core.infrastructure.archive import EDUCASE_EXT, EDURESULT_EXT


def test_core_version_present() -> None:
    assert educase_core.__version__


def test_archive_extensions() -> None:
    assert EDUCASE_EXT == ".educase"
    assert EDURESULT_EXT == ".eduresult"
