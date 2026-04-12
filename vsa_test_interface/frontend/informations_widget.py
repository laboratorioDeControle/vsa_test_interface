from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox


class InformationsWidget(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self.setTitle("Informações:")

    def __init_backend__(self):
        pass