from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit, QPushButton, QComboBox


class AutonomousMissionWidget(QGroupBox):
    @property
    def mission_time(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_mission_time.text())

            if result <= 0:
                result = 1.0

        except ValueError:
            pass

        finally:
            self._le_mission_time.setText(str(result))
            return result
        
    @property
    def mission_start_delay(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_mission_start_delay.text())

            if result < 0:
                result = 0.0

        except ValueError:
            pass

        finally:
            self._le_mission_start_delay.setText(str(result))
            return result

    @property
    def thruster_power(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_thruster_power.text())

            if self.thruster_unit == "%":
                result = result / 100.0
            else:
                a: float = self.thruster_calib[0]
                b: float = self.thruster_calib[1]

                result = ((result * a) + b) / 100.0

        except ValueError:
            pass

        finally:
            print(result)
            return result

    
    @property
    def horizontal_rudders_angle(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_horizontal_rudders.text())
        except ValueError:
            pass

        finally:
            self._le_horizontal_rudders.setText(str(result))
            return result
        
    
    @property
    def vertical_rudders_angle(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_vertical_rudders.text())
        except ValueError:
            pass

        finally:
            self._le_vertical_rudders.setText(str(result))
            return result
    
    @property
    def cycle_frequency(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_cycle_frequency.text())

            if result <= 0.0:
                result = 1.0

        except ValueError:
            pass

        finally:
            self._le_cycle_frequency.setText(str(result))
            return result

    @property
    def bt_send_mission_parameters(self) -> QPushButton:
        return self._bt_send_mission

    @property
    def thruster_calib(self) -> list:
        return self._thurster_calib

    @thruster_calib.setter
    def thruster_calib(self, value: list):
        self._thurster_calib[0] = value[0]
        self._thurster_calib[1] = value[1]

    @property
    def thruster_unit(self) -> str:
        return self._cb_thruster_unit.currentText()


    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()
        
        self._le_mission_time: QLineEdit = QLineEdit("1.0")
        self._le_mission_start_delay: QLineEdit = QLineEdit("0.0")

        self._le_thruster_power: QLineEdit = QLineEdit("0.0")
        self._le_horizontal_rudders: QLineEdit = QLineEdit("15.0")
        self._le_vertical_rudders: QLineEdit = QLineEdit("0.0")
        self._le_cycle_frequency: QLineEdit = QLineEdit("1.0")

        self._bt_send_mission: QPushButton = QPushButton("Enviar Missão")

        self._cb_thruster_unit: QComboBox = QComboBox()

        self._thurster_calib: list = [1, 0]

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        for unit in ["%", "m/s"]:
            self._cb_thruster_unit.addItem(unit)

        self._layout.addWidget(QLabel("Tempo da Missão:"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_mission_time, 0, 1, 1, 1)
        self._layout.addWidget(QLabel("segundos"), 0, 2, 1, 1)

        self._layout.addWidget(QLabel("Atraso de Início da Missão:"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_mission_start_delay, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("segundos"), 1, 2, 1, 1)

        self._layout.addWidget(QLabel("Potência do Thruster:"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_thruster_power, 2, 1, 1, 1)
        self._layout.addWidget(self._cb_thruster_unit, 2, 2, 1, 1)

        self._layout.addWidget(QLabel("Ângulo dos Lemes Verticais:"), 3, 0, 1, 1)
        self._layout.addWidget(self._le_vertical_rudders, 3, 1, 1, 1)
        self._layout.addWidget(QLabel("graus"), 3, 2, 1, 1)

        self._layout.addWidget(QLabel("Ângulo dos Lemes Horizontais:"), 4, 0, 1, 1)
        self._layout.addWidget(self._le_horizontal_rudders, 4, 1, 1, 1)
        self._layout.addWidget(QLabel("graus"), 4, 2, 1, 1)

        self._layout.addWidget(QLabel("Frequência das Oscilações:"), 5, 0, 1, 1)
        self._layout.addWidget(self._le_cycle_frequency, 5, 1, 1, 1)
        self._layout.addWidget(QLabel("Hz"), 5, 2, 1, 1)

        self._layout.addWidget(self._bt_send_mission, 6, 0, 1, 3)

    def __init_backend__(self):
        pass