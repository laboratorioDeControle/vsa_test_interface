import time

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QSplashScreen, QProgressBar
from PyQt5.QtGui import Qt, QPixmap


def open_file_dialog(parent: QWidget, title: str, file_description: str, file_extension) -> str:
    filter_file: str = file_description + " (*" + file_extension + ")"
    file_path: tuple = QFileDialog.getSaveFileName(parent, title, filter=filter_file)
    return file_path[0]


def save_file_dialog(parent: QWidget, title: str, file_description: str, file_extension) -> str:
    filter_file: str = file_description + " (*" + file_extension + ")"
    file_path: tuple = QFileDialog.getOpenFileName(parent, title, filter=filter_file)
    return file_path[0]


def info_ok_dialog(parent: QWidget, title: str, message: str):
    dlg: QMessageBox = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(message)

    dlg.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.exec()


def question_yes_no_dialog(parent: QWidget, title: str, message: str) -> bool:
    result = False

    dlg: QMessageBox = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(message)

    dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    dlg.setIcon(QMessageBox.Icon.Question)
    _result = dlg.exec()

    if _result == QMessageBox.Yes:
        result = True

    return result


class SplashScreen(QSplashScreen):
    def __init__(self, image_path: str, progress_bar_step_time: float):
        super().__init__()

        self._image_path: str = image_path
        self._progress_bar_step_time: float = progress_bar_step_time

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setPixmap(QPixmap(self._image_path))

    def progress(self):
        for i in range(100):
            time.sleep(self._progress_bar_step_time)
