"""Главное окно Constructor: редактор кейса + сохранение в .educase."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from educase_constructor.ui.case_editor import CaseEditor
from educase_core.application.case_builder import build_case
from educase_core.application.cases import save_case


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EduCase Constructor")
        self.resize(1000, 700)

        self.editor = CaseEditor(self)
        self.setCentralWidget(self.editor)
        self._build_menu()

    def _build_menu(self) -> None:
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        if file_menu is None:
            return
        save_action = QAction("Сохранить кейс…", self)
        save_action.triggered.connect(self.save_case_dialog)
        file_menu.addAction(save_action)

    def save_case_dialog(self) -> None:
        """Показать диалог сохранения и записать кейс в выбранный .educase."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить кейс",
            "",
            "Кейсы EduCase (*.educase)",
        )
        if path:
            self.save_case_to_path(Path(path))

    def save_case_to_path(self, path: Path) -> bool:
        """Собрать кейс из редактора и записать в .educase.

        Тестируемый шов: вызывается без диалога выбора файла. При пустом идентификаторе
        кейса (``build_case`` бросает ``ValueError``) — предупреждение и ``False``, файл не
        пишется. Запись синхронная: архив маленький и локальный — QThread не нужен.
        """
        draft = self.editor.to_draft()
        try:
            case = build_case(draft)
        except ValueError as exc:
            QMessageBox.warning(self, "Не удалось сохранить", str(exc))
            return False
        save_case(case, path)
        return True
