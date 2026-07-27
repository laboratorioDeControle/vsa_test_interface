from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QCheckBox, QTabWidget, QPushButton
from .widgets.calib_thruster_widget import CalibThrusterWidget


class CalibrationWidget(QWidget):
    @property
    def calib_thruster(self) -> CalibThrusterWidget:
        return self._calib_thruster

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()
        self._tab: QTabWidget = QTabWidget()

        self._calib_thruster: CalibThrusterWidget = CalibThrusterWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self._tab.addTab(self._calib_thruster, "Thruster")

        self._layout.addWidget(self._tab, 0, 0, 1, 1)

    def __init_backend__(self):
        pass

    def serialize(self) -> dict:
        return {
            "trusther": self.calib_thruster.serialize()
        }

    def deserialize(self, paremeters: dict):
        if "trusther" in paremeters.keys():
            self.calib_thruster.deserialize(paremeters["trusther"])
