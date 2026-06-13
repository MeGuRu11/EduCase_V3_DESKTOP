"""Тесты ``read_asset_sources``: I/O-сбор байтов ассетов драфта (Qt-free)."""
from __future__ import annotations

from pathlib import Path

import pytest

from educase_core.application.assets import read_asset_sources
from educase_core.application.case_builder import (
    AssetRef,
    CaseDraft,
    ContactsDraft,
    EnvironmentDraft,
)


def test_reads_scheme_bytes(tmp_path: Path) -> None:
    """Заданная ``contacts.scheme`` → ``{asset_id: те же байты файла}``."""
    source = tmp_path / "scheme.png"
    source.write_bytes(b"\x89PNG-bytes")

    draft = CaseDraft(
        case_id="case-a",
        contacts=ContactsDraft(scheme=AssetRef("a1.png", str(source))),
    )
    assets = read_asset_sources(draft)

    assert assets == {"a1.png": b"\x89PNG-bytes"}


def test_reads_contacts_and_environment_schemes(tmp_path: Path) -> None:
    """Обе схемы (этапы 3 и 4) собираются в один словарь по своим id."""
    contacts_src = tmp_path / "contacts.png"
    contacts_src.write_bytes(b"CONTACTS")
    env_src = tmp_path / "env.jpg"
    env_src.write_bytes(b"ENV")

    draft = CaseDraft(
        case_id="case-b",
        contacts=ContactsDraft(scheme=AssetRef("c1.png", str(contacts_src))),
        environment=EnvironmentDraft(scheme=AssetRef("e1.jpg", str(env_src))),
    )
    assets = read_asset_sources(draft)

    assert assets == {"c1.png": b"CONTACTS", "e1.jpg": b"ENV"}


def test_empty_scheme_gives_empty_dict() -> None:
    """Драфт без ассетов → пустой словарь."""
    draft = CaseDraft(case_id="case-c", contacts=ContactsDraft())
    assert read_asset_sources(draft) == {}


def test_missing_source_raises_oserror(tmp_path: Path) -> None:
    """Несуществующий ``source_path`` → ``OSError`` пробрасывается наверх."""
    draft = CaseDraft(
        case_id="case-d",
        contacts=ContactsDraft(scheme=AssetRef("x1.png", str(tmp_path / "ghost.png"))),
    )
    with pytest.raises(OSError):
        read_asset_sources(draft)
