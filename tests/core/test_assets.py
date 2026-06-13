"""Тесты ``read_asset_sources``: I/O-сбор байтов ассетов драфта (Qt-free)."""
from __future__ import annotations

from pathlib import Path

import pytest

from educase_core.application.assets import read_asset_sources
from educase_core.application.case_builder import (
    AssetRef,
    CaseDraft,
    ClinicalDraft,
    ContactsDraft,
    EnvironmentDraft,
    FinalDraft,
    PatientDraft,
    SearchDraft,
    SearchEntryDraft,
    SesDraft,
    SynonymSetDraft,
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


def _reveal_search(asset_id: str, source: Path) -> SearchDraft:
    """Поиск с одной точкой (непустой канон) и одним изображением вскрытия — для тестов этапов."""
    return SearchDraft(
        entries=(
            SearchEntryDraft(
                triggers=SynonymSetDraft(canonical="триггер"),
                reveal_assets=(AssetRef(asset_id, str(source)),),
            ),
        ),
    )


def test_reads_assets_from_all_locations(tmp_path: Path) -> None:
    """Ассеты из всех мест драфта (включая reveal всех трёх этапов с поиском) — в один словарь."""
    patient_src = tmp_path / "patient.png"
    patient_src.write_bytes(b"PATIENT")
    scheme_src = tmp_path / "scheme.png"
    scheme_src.write_bytes(b"SCHEME")
    photo_src = tmp_path / "photo.jpg"
    photo_src.write_bytes(b"PHOTO")
    clinical_src = tmp_path / "clinical.png"
    clinical_src.write_bytes(b"CLINICAL")
    ses_src = tmp_path / "ses.png"
    ses_src.write_bytes(b"SES")
    final_src = tmp_path / "final.png"
    final_src.write_bytes(b"FINAL")

    draft = CaseDraft(
        case_id="case-all",
        patients=(
            PatientDraft(id="p1", title="П1", assets=(AssetRef("pa.png", str(patient_src)),)),
        ),
        contacts=ContactsDraft(scheme=AssetRef("sc.png", str(scheme_src))),
        environment=EnvironmentDraft(photos=(AssetRef("ph.jpg", str(photo_src)),)),
        clinical=ClinicalDraft(search=_reveal_search("cl.png", clinical_src)),
        ses=SesDraft(search=_reveal_search("se.png", ses_src)),
        final=FinalDraft(search=_reveal_search("fi.png", final_src)),
    )
    assets = read_asset_sources(draft)

    # Точный словарь: пропадание любого из трёх reveal-этапов сломает сравнение.
    assert assets == {
        "pa.png": b"PATIENT",
        "sc.png": b"SCHEME",
        "ph.jpg": b"PHOTO",
        "cl.png": b"CLINICAL",
        "se.png": b"SES",
        "fi.png": b"FINAL",
    }


def test_reveal_assets_of_dropped_entry_not_packed(tmp_path: Path) -> None:
    """Точка поиска с пустым каноном отбрасывается билдером → её ассет в архив НЕ пакуется."""
    reveal_src = tmp_path / "orphan.png"
    reveal_src.write_bytes(b"ORPHAN")

    draft = CaseDraft(
        case_id="case-orphan",
        clinical=ClinicalDraft(
            search=SearchDraft(
                entries=(
                    SearchEntryDraft(
                        triggers=SynonymSetDraft(canonical="   "),  # пустой → точка отброшена
                        reveal_assets=(AssetRef("or.png", str(reveal_src)),),
                    ),
                ),
            ),
        ),
    )
    assert read_asset_sources(draft) == {}


def test_duplicate_asset_id_deduplicated(tmp_path: Path) -> None:
    """Повтор одного ``asset_id`` в разных местах → один ключ (естественный дедуп словаря)."""
    source = tmp_path / "shared.png"
    source.write_bytes(b"SHARED")
    ref = AssetRef("dup.png", str(source))

    draft = CaseDraft(
        case_id="case-dup",
        patients=(PatientDraft(id="p1", title="П1", assets=(ref,)),),
        environment=EnvironmentDraft(photos=(ref,)),
    )
    assets = read_asset_sources(draft)

    assert assets == {"dup.png": b"SHARED"}
