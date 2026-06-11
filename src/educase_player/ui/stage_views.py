"""Фабрика виджетов этапов: индивидуальная сборка по типу этапа (ADR-004)."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from educase_core.domain.stages import (
    Stage,
    StageClinical,
    StageContacts,
    StageEnvironment,
    StageFinal,
    StagePatients,
    StageSes,
)
from educase_player.ui.branch_widget import BranchWidget
from educase_player.ui.document_field_widget import DocumentFieldWidget
from educase_player.ui.document_widget import DocumentWidget
from educase_player.ui.inspection_widget import InspectionWidget
from educase_player.ui.patient_card_widget import PatientCardWidget
from educase_player.ui.search_widget import SearchWidget
from educase_player.ui.timeline_widget import TimelineWidget


def build_stage_view(stage: Stage) -> QWidget:
    """Создать прокручиваемый виджет для этапа по его типу (шесть фиксированных, ADR-004)."""
    container = QWidget()
    outer = QVBoxLayout(container)
    outer.setContentsMargins(0, 0, 0, 0)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    outer.addWidget(scroll)

    inner = QWidget()
    layout = QVBoxLayout(inner)
    scroll.setWidget(inner)

    title_label = QLabel(stage.title)
    layout.addWidget(title_label)

    if stage.intro:
        intro_label = QLabel(stage.intro)
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

    has_content = False

    if isinstance(stage, StagePatients):
        if stage.search is not None and stage.search.entries:
            layout.addWidget(SearchWidget(stage.search))
            has_content = True
        for card in stage.patients:
            layout.addWidget(PatientCardWidget(card))
            has_content = True

    elif isinstance(stage, StageClinical):
        if stage.search is not None and stage.search.entries:
            layout.addWidget(SearchWidget(stage.search))
            has_content = True
        if stage.branch is not None:
            layout.addWidget(BranchWidget(stage.branch))
            has_content = True
        for task in stage.documents:
            layout.addWidget(DocumentWidget(task))
            has_content = True

    elif isinstance(stage, StageContacts):
        if stage.scheme is not None:
            stub = QLabel(f"Схема: {stage.scheme}")  # TODO ADR-012
            stub.setEnabled(False)
            layout.addWidget(stub)
            has_content = True
        if stage.inspection is not None:
            layout.addWidget(InspectionWidget(stage.inspection))
            has_content = True

    elif isinstance(stage, StageEnvironment):
        if stage.scheme is not None:
            stub = QLabel(f"Схема: {stage.scheme}")  # TODO ADR-012
            stub.setEnabled(False)
            layout.addWidget(stub)
            has_content = True
        if stage.photos:
            photo_ids = ", ".join(stage.photos)
            photos_stub = QLabel(f"Фото: {photo_ids}")  # TODO ADR-012
            photos_stub.setEnabled(False)
            layout.addWidget(photos_stub)
            has_content = True
        for task in stage.documents:
            layout.addWidget(DocumentWidget(task))
            has_content = True
        if stage.inspection is not None:
            layout.addWidget(InspectionWidget(stage.inspection))
            has_content = True

    elif isinstance(stage, StageSes):
        if stage.search is not None and stage.search.entries:
            layout.addWidget(SearchWidget(stage.search))
            has_content = True
        if stage.level_choice is not None:
            layout.addWidget(DocumentFieldWidget(stage.level_choice))
            has_content = True
        for task in stage.documents:
            layout.addWidget(DocumentWidget(task))
            has_content = True

    elif isinstance(stage, StageFinal):
        if stage.search is not None and stage.search.entries:
            layout.addWidget(SearchWidget(stage.search))
            has_content = True
        for task in stage.documents:
            layout.addWidget(DocumentWidget(task))
            has_content = True
        for tl in stage.timelines:
            layout.addWidget(TimelineWidget(tl))
            has_content = True

    if not has_content:
        layout.addWidget(QLabel("Нет заданий на этом этапе"))

    layout.addStretch()

    return container
