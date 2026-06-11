"""Тесты сборки ``Case`` из ``CaseDraft`` (CONSTRUCTOR-01, слой приложения)."""
from __future__ import annotations

import pytest

from educase_core.application.case_builder import CaseDraft, PatientDraft, build_case
from educase_core.domain import StageClinical, StageFinal


def test_build_case_with_meta_and_patients() -> None:
    """Мета и два ``PatientDraft`` → корректный ``Case`` с двумя ``PatientCard``."""
    draft = CaseDraft(
        case_id="case-1",
        title="Вспышка ОКИ",
        author="Иванов",
        nosology="Сальмонеллёз",
        unit_personnel=150,
        patients=(
            PatientDraft(id="p1", title="Пациент 1", fields=(("Возраст", "25"),)),
            PatientDraft(id="p2", title="Пациент 2", assets=("img_01",)),
        ),
    )
    case = build_case(draft)

    assert case.meta.id == "case-1"
    assert case.meta.title == "Вспышка ОКИ"
    assert case.meta.author == "Иванов"
    assert case.meta.nosology == "Сальмонеллёз"
    assert case.meta.unit_personnel == 150
    assert case.meta.created_at  # ISO-дата проставлена
    assert len(case.patients.patients) == 2
    assert case.patients.patients[0].id == "p1"
    assert case.patients.patients[0].fields == (("Возраст", "25"),)
    assert case.patients.patients[1].assets == ("img_01",)
    # Остальные этапы — дефолтные пустые.
    assert case.clinical == StageClinical()
    assert case.final == StageFinal()
    assert case.patients.search is None


def test_build_case_empty_id_raises() -> None:
    """Пустой (или пробельный) идентификатор кейса → ``ValueError``."""
    with pytest.raises(ValueError):
        build_case(CaseDraft(case_id="   "))


def test_build_case_unit_personnel_none() -> None:
    """``unit_personnel=None`` пробрасывается в мету без подмены на 0."""
    case = build_case(CaseDraft(case_id="case-2", unit_personnel=None))
    assert case.meta.unit_personnel is None
