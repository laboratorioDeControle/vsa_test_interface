from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from .ihm_main_widget import IHMMainWidget


class IHMWindow(QMainWindow):
    @property
    def main_widget(self) -> IHMMainWidget:
        return self._main_widget

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._main_widget: IHMMainWidget = IHMMainWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setWindowTitle("VSA Test Interface - Marinha do Brasil")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._main_widget)

    def __init_backend__(self):
        pass

