from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit


class ManualMissionWidget(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._le_thruster_power: QLineEdit = QLineEdit("0.0")
        self._le_vertical_rudders: QLineEdit = QLineEdit("0.0")
        self._le_horizontal_rudders: QLineEdit = QLineEdit("0.0")

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self.setTitle("Manual:")

        self._layout.addWidget(QLabel("Potência do Thruster:"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_thruster_power, 0, 1, 1, 1)
        self._layout.addWidget(QLabel("%"), 0, 2, 1, 1)

        self._layout.addWidget(QLabel("Ângulo dos Lemes Verticais:"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_vertical_rudders, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("graus"), 1, 2, 1, 1)

        self._layout.addWidget(QLabel("Ângulo dos Lemes Horizontais:"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_horizontal_rudders, 2, 1, 1, 1)
        self._layout.addWidget(QLabel("graus"), 2, 2, 1, 1)

    def __init_backend__(self):
        pass