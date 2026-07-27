import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from ...backend.tools import poly_list_to_poly_text, calculate_calibration_parameters


class CalibResultsWidget(QGroupBox):
    @property
    def r2(self) -> float:
        return self._r2

    @r2.setter
    def r2(self, value: float):
        self._r2 = value
        self._lbl_r_2.setText("%.4f" % value)

    @property
    def poly(self) -> str:
        return self._poly

    @poly.setter
    def poly(self, value: list):
        print(value)
        self._poly_coef = value
        poly: str = poly_list_to_poly_text(self._poly_coef, "x")
        self._lbl_poly.setText(poly)

        self.a = self._poly_coef[0]
        self.b = self._poly_coef[1]

    @property
    def poly_coef(self) -> list:
        return self._poly_coef

    @property
    def a(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_a.text())
        except ValueError:
            pass
        finally:
            self._le_a.setText(str(result))
            return result

    @a.setter
    def a(self, value: float):
        self._le_a.setText(str(value))

    @property
    def b(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_b.text())
        except ValueError:
            pass
        finally:
            self._le_b.setText(str(result))
            return result

    @b.setter
    def b(self, value: float):
        self._le_b.setText(str(value))

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()
        self._lbl_poly: QLabel = QLabel()
        self._lbl_r_2: QLabel = QLabel()

        self._le_a: QLineEdit = QLineEdit("1.0")
        self._le_b: QLineEdit = QLineEdit("0.0")

        self._r2: float = 0.0
        self._poly_coef: list = []
        self._poly: str = ""

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setTitle("Resultado:")
        self.setLayout(self._layout)

        self._lbl_poly.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._lbl_poly.setCursor(QCursor(Qt.CursorShape.IBeamCursor))

        self._layout.addWidget(QLabel("a:"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_a, 0, 1, 1, 1)
        self._layout.addWidget(QLabel("b:"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_b, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("Polinômio:"), 2, 0, 1, 1)
        self._layout.addWidget(self._lbl_poly, 2, 1, 1, 1)
        self._layout.addWidget(QLabel("R²:"), 3, 0, 1, 1)
        self._layout.addWidget(self._lbl_r_2, 3, 1, 1, 1)

    def __init_backend__(self):
        pass

    def calculate(self, refs_and_measurements: dict):
        result: dict = calculate_calibration_parameters(refs_and_measurements)

        self.poly = result["interpolation_poly_coef"]
        self.r2 = result["r2"]

    def clear(self):
        self._lbl_poly.setText("")
        self._lbl_r_2.setText("")

    def serialize(self) -> dict:
        return {
            "interpolation_poly_coef": [self.a, self.b],
            "r2": self.r2
        }

    def deserialize(self, parameters: dict):
        if "interpolation_poly_coef" in parameters.keys():
            if len(parameters["interpolation_poly_coef"]) >= 2:
                self.poly = parameters["interpolation_poly_coef"]

        if "r2" in parameters.keys():
            if parameters["r2"] != 0.0:
                self.r2 = parameters["r2"]