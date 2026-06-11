"""Сборка доменного ``Case`` из «сырых» значений UI (этот срез: мета + этап «Пациенты»).

UI собирает значения виджетов в простые ``*Draft``-структуры, а доменные тонкости
(неизменяемость, конструирование этапов) живут здесь. Чистые функции без I/O — обратная
сторона (из ``Case`` в ``CaseDraft`` для будущего редактирования) пока не реализуется.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from educase_core.domain import Case, CaseMeta, PatientCard, StagePatients


@dataclass(frozen=True)
class PatientDraft:
    """Сырые значения одной карточки пациента из UI."""

    id: str
    title: str
    fields: tuple[tuple[str, str], ...] = ()
    assets: tuple[str, ...] = ()


@dataclass(frozen=True)
class CaseDraft:
    """Сырые значения кейса из UI (этот срез: мета + пациенты)."""

    case_id: str
    title: str = ""
    author: str = ""
    nosology: str = ""
    unit_personnel: int | None = None
    patients: tuple[PatientDraft, ...] = ()


def build_case(draft: CaseDraft) -> Case:
    """Собрать доменный ``Case`` из ``CaseDraft``.

    Валидируется только обязательный непустой идентификатор кейса. Остальные пять этапов —
    дефолтные пустые: этот срез трогает лишь мету и этап «Пациенты». Чистая функция без I/O.
    """
    case_id = draft.case_id.strip()
    if not case_id:
        raise ValueError("нужен идентификатор кейса")

    meta = CaseMeta(
        id=case_id,
        title=draft.title,
        author=draft.author,
        nosology=draft.nosology,
        unit_personnel=draft.unit_personnel,
        created_at=date.today().isoformat(),
    )
    patients = StagePatients(
        patients=tuple(
            PatientCard(id=p.id, title=p.title, fields=p.fields, assets=p.assets)
            for p in draft.patients
        )
    )
    return Case(meta=meta, patients=patients)


__all__ = ["CaseDraft", "PatientDraft", "build_case"]
