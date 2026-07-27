from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from .ihm_main_widget import IHMMainWidget
from ..backend.tools import dict_to_json, json_to_dict


class IHMWindow(QMainWindow):
    @property
    def main_widget(self) -> IHMMainWidget:
        return self._main_widget

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._main_widget: IHMMainWidget = IHMMainWidget()

        self.__init_ui__()
        self.__init_backend__()
        self.deserialize()

    def __init_ui__(self):
        self.setWindowTitle("Interface de Teste do VSA - Marinha do Brasil")
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self._main_widget)

    def __init_backend__(self):
        pass

    def closeEvent(self, a0):
        self.serialize()
        return super().closeEvent(a0)

    def serialize(self):
        serialization: dict = self.main_widget.serialize()
        dict_to_json("parameters", serialization)

    def deserialize(self):
        serialization: dict = json_to_dict("parameters.json")
        if serialization != {}:
            self.main_widget.deserialize(serialization)


