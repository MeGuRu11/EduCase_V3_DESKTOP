"""Редактор кейса целиком для текущего среза: мета + этап «Пациенты» (Constructor).

Без визуальной полировки: только функциональные виджеты и layout-менеджеры. Публичные поля
меты, список редакторов пациентов и кнопки — точки доступа для тестов. Сборка в домен —
через ``to_draft`` (далее ``build_case`` из слоя приложения).
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from educase_constructor.ui.clinical_editor import ClinicalEditor
from educase_constructor.ui.contacts_editor import ContactsEditor
from educase_constructor.ui.environment_editor import EnvironmentEditor
from educase_constructor.ui.final_editor import FinalEditor
from educase_constructor.ui.patient_editor import PatientEditor
from educase_constructor.ui.ses_editor import SesEditor
from educase_core.application.case_builder import CaseDraft


class CaseEditor(QWidget):
    """Редактор меты кейса и всех шести этапов прохождения."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.case_id_edit = QLineEdit(self)
        self.title_edit = QLineEdit(self)
        self.author_edit = QLineEdit(self)
        self.nosology_edit = QLineEdit(self)
        self.unit_personnel_edit = QLineEdit(self)

        self.patient_editors: list[PatientEditor] = []

        meta_form = QFormLayout()
        meta_form.addRow("Идентификатор кейса", self.case_id_edit)
        meta_form.addRow("Название", self.title_edit)
        meta_form.addRow("Автор", self.author_edit)
        meta_form.addRow("Нозология", self.nosology_edit)
        meta_form.addRow("Личный состав", self.unit_personnel_edit)

        self.add_patient_button = QPushButton("Добавить пациента", self)
        self.remove_patient_button = QPushButton("Удалить последнего", self)
        self.add_patient_button.clicked.connect(self.add_patient)
        self.remove_patient_button.clicked.connect(self.remove_last_patient)

        patient_buttons = QHBoxLayout()
        patient_buttons.addWidget(self.add_patient_button)
        patient_buttons.addWidget(self.remove_patient_button)

        self._patients_layout = QVBoxLayout()

        patients_box = QGroupBox("Пациенты")
        patients_box_layout = QVBoxLayout(patients_box)
        patients_box_layout.addLayout(patient_buttons)
        patients_box_layout.addLayout(self._patients_layout)

        self.clinical_editor = ClinicalEditor(self)
        self.contacts_editor = ContactsEditor(self)
        self.environment_editor = EnvironmentEditor(self)
        self.ses_editor = SesEditor(self)
        self.final_editor = FinalEditor(self)

        # Вкладка «Кейс и пациенты»: мета-форма + блок пациентов.
        case_tab = QWidget()
        case_tab_layout = QVBoxLayout(case_tab)
        case_tab_layout.addLayout(meta_form)
        case_tab_layout.addWidget(patients_box)
        case_tab_layout.addStretch(1)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(self._scroll_tab(case_tab), "Кейс и пациенты")
        self.tabs.addTab(self._scroll_tab(self.clinical_editor), "Клинический")
        self.tabs.addTab(self._scroll_tab(self.contacts_editor), "Контакты")
        self.tabs.addTab(self._scroll_tab(self.environment_editor), "Среда")
        self.tabs.addTab(self._scroll_tab(self.ses_editor), "СЭС")
        self.tabs.addTab(self._scroll_tab(self.final_editor), "Финал")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

    def _scroll_tab(self, content: QWidget) -> QScrollArea:
        """Обернуть содержимое вкладки в прокручиваемую область.

        ``setWidgetResizable(True)`` растягивает контент по ширине области и даёт
        вертикальную прокрутку высоким редакторам вместо их сжатия.
        """
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        return scroll

    def add_patient(self) -> None:
        """Добавить редактор нового пациента в конец списка."""
        editor = PatientEditor(self)
        self.patient_editors.append(editor)
        self._patients_layout.addWidget(editor)

    def remove_last_patient(self) -> None:
        """Удалить последний редактор пациента (если он есть)."""
        if not self.patient_editors:
            return
        editor = self.patient_editors.pop()
        self._patients_layout.removeWidget(editor)
        editor.deleteLater()

    def _unit_personnel(self) -> int | None:
        text = self.unit_personnel_edit.text().strip()
        if not text:
            return None
        try:
            return int(text)
        except ValueError:
            return None

    def to_draft(self) -> CaseDraft:
        """Собрать ``CaseDraft`` из меты и всех редакторов пациентов."""
        return CaseDraft(
            case_id=self.case_id_edit.text(),
            title=self.title_edit.text(),
            author=self.author_edit.text(),
            nosology=self.nosology_edit.text(),
            unit_personnel=self._unit_personnel(),
            patients=tuple(editor.to_draft() for editor in self.patient_editors),
            clinical=self.clinical_editor.to_draft(),
            contacts=self.contacts_editor.to_draft(),
            environment=self.environment_editor.to_draft(),
            ses=self.ses_editor.to_draft(),
            final=self.final_editor.to_draft(),
        )
