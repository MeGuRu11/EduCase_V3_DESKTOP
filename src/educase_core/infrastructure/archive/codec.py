"""Заготовка кодека ZIP-архивов обмена. Реализацию ведёт senior-developer (Opus).

ВНИМАНИЕ: никакого сетевого I/O. Только локальная файловая система.
"""
from __future__ import annotations

from pathlib import Path

from educase_core.infrastructure.archive import EDUCASE_EXT, EDURESULT_EXT


def write_educase(payload: dict[str, object], dst: Path) -> Path:
    """Упаковать кейс в .educase (ZIP с manifest.json + ассеты). TODO: реализовать."""
    raise NotImplementedError("Реализуется в задаче по educase-archive-format")


def read_educase(src: Path) -> dict[str, object]:
    """Прочитать и провалидировать .educase. TODO: реализовать."""
    raise NotImplementedError("Реализуется в задаче по educase-archive-format")


def write_eduresult(payload: dict[str, object], dst: Path) -> Path:
    """Упаковать результат прохождения в .eduresult. TODO: реализовать."""
    raise NotImplementedError("Реализуется в задаче по educase-archive-format")


__all__ = ["EDUCASE_EXT", "EDURESULT_EXT", "read_educase", "write_educase", "write_eduresult"]
