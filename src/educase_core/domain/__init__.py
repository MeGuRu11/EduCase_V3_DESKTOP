"""Доменный слой. НИКАКИХ внешних зависимостей (ни PySide6, ни ORM, ни сети).

Публичный API доменной модели Case/Stage. Каждая сущность сериализуется чистыми
``to_dict``/``from_dict`` (документная модель, ADR-009).
"""
from educase_core.domain.assets import AssetKind, AssetRef
from educase_core.domain.case import Case, CaseMeta
from educase_core.domain.documents import (
    ChoiceMatch,
    DateMatch,
    DocumentField,
    DocumentOption,
    DocumentTask,
    DocumentTemplate,
    FieldType,
    MatchRule,
    NumberMatch,
    TextMatch,
    match_rule_from_dict,
)
from educase_core.domain.epidemiology import (
    SesLevel,
    classify_ses,
    extensive_indicator,
    intensive_indicator,
    intensive_indicator_period,
)
from educase_core.domain.search import (
    InspectionCheck,
    KeywordSearch,
    SearchEntry,
    SynonymSet,
)
from educase_core.domain.stages import (
    BranchOption,
    BranchPoint,
    PatientCard,
    Stage,
    StageClinical,
    StageContacts,
    StageEnvironment,
    StageFinal,
    StageKind,
    StagePatients,
    StageSes,
    Timeline,
)

__all__ = [
    "AssetKind",
    "AssetRef",
    "BranchOption",
    "BranchPoint",
    "Case",
    "CaseMeta",
    "ChoiceMatch",
    "DateMatch",
    "DocumentField",
    "DocumentOption",
    "DocumentTask",
    "DocumentTemplate",
    "FieldType",
    "InspectionCheck",
    "KeywordSearch",
    "MatchRule",
    "NumberMatch",
    "PatientCard",
    "SearchEntry",
    "SesLevel",
    "Stage",
    "StageClinical",
    "StageContacts",
    "StageEnvironment",
    "StageFinal",
    "StageKind",
    "StagePatients",
    "StageSes",
    "SynonymSet",
    "TextMatch",
    "Timeline",
    "classify_ses",
    "extensive_indicator",
    "intensive_indicator",
    "intensive_indicator_period",
    "match_rule_from_dict",
]
