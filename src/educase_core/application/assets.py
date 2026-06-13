"""Сбор байтов ассетов кейса из исходных файлов (слой приложения).

Единственное место чтения файлов в цепочке сборки кейса: ``build_case`` и ``build_*`` —
чистые функции без I/O, поэтому чтение байтов ассетов вынесено сюда. Обход драфта собирает
все ``AssetRef`` и читает их исходные файлы по ``source_path``. В этом срезе ассеты несут
только схемы этапов 3 и 4 (``contacts.scheme`` / ``environment.scheme``).
"""
from __future__ import annotations

from pathlib import Path

from educase_core.application.case_builder import AssetRef, CaseDraft


def _collect_asset_refs(draft: CaseDraft) -> list[AssetRef]:
    """Собрать все ``AssetRef`` драфта (в этом срезе — схемы этапов 3 и 4, если заданы)."""
    refs: list[AssetRef] = []
    if draft.contacts is not None and draft.contacts.scheme is not None:
        refs.append(draft.contacts.scheme)
    if draft.environment is not None and draft.environment.scheme is not None:
        refs.append(draft.environment.scheme)
    return refs


def read_asset_sources(draft: CaseDraft) -> dict[str, bytes]:
    """Прочитать байты исходных файлов всех ассетов драфта в ``{asset_id: bytes}``.

    Обходит драфт, для каждого ``AssetRef`` читает ``Path(ref.source_path).read_bytes()``.
    ``OSError`` (нет файла/нет доступа) пробрасывается наверх — обработает окно. Если ассетов
    нет — пустой словарь.
    """
    return {
        ref.asset_id: Path(ref.source_path).read_bytes()
        for ref in _collect_asset_refs(draft)
    }


__all__ = ["read_asset_sources"]
