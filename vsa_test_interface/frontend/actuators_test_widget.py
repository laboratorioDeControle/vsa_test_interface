from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit, QPushButton, QCheckBox
import math

class ActuatorsTestWidget(QGroupBox):
    @property
    def thruster(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_thruster.text())
            if result <= -1.0:
                result = -1.0
            elif result >= 1.0:
                result = 1.0

        except ValueError:
            pass

        finally:
            self._le_thruster.setText(str(result))
            return result
        

    @property
    def servo_top(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_top.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_top.setText(str(result))
            return result

    @property
    def servo_right(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_right.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_right.setText(str(result))
            return result

    @property
    def servo_bottom(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_bottom.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_bottom.setText(str(result))
            return result

    @property
    def servo_left(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_left.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_left.setText(str(result))
            return result

    @property
    def top_offset(self) -> float:
        """Offset top in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_top_offset.text())
        except ValueError:
            pass
        finally:
            self._le_top_offset.setText(str(result))
            return result

    @property
    def right_offset(self) -> float:
        """Offset for right in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_right_offset.text())
        except ValueError:
            pass
        finally:
            self._le_right_offset.setText(str(result))
            return result

    @property
    def bottom_offset(self) -> float:
        """Offset for bottom in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_bottom_offset.text())
        except ValueError:
            pass
        finally:
            self._le_bottom_offset.setText(str(result))
            return result

    @property
    def left_offset(self) -> float:
        """Offset for left in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_left_offset.text())
        except ValueError:
            pass
        finally:
            self._le_left_offset.setText(str(result))
            return result

    @property
    def bt_send_command(self) -> QPushButton:
        return self._bt_send_commands

    @property
    def bt_send_offsets(self) -> QPushButton:
        return self._bt_send_offsets

    @property
    def bt_start_stop_cycle(self) -> QPushButton:
        return self._bt_start_stop_cycle

    @property
    def send_frequency(self) -> float:
        result: float = 1.0

        try:
            result = float(self._le_send_frequency.text())

            if result <= 0:
                result = 1.0

        except ValueError:
            pass

        finally:
            self._le_send_frequency.setText(str(result))
            return result

    @property
    def send_period(self) -> float:
        return 1.0 / self.send_frequency

    @property
    def rudders_msg(self) -> list:
        result: list = [
            math.radians(self.servo_left),
            math.radians(self.servo_bottom),
            math.radians(self.servo_right),
            math.radians(self.servo_top)
        ]

        return result

    @property
    def thrusters_msg(self) -> list:
        result: list = [
            float(self.thruster)
        ]

        return result

    @property
    def periodic_send(self) -> bool:
        return self._chb_cycle_send.isChecked()

    @property
    def send_started(self) -> bool:
        return self._send_started

    @send_started.setter
    def send_started(self, value: bool):
        self._send_started = value

        if value:
            self.bt_send_command.setText("Parar Envio")
            self._le_send_frequency.setEnabled(False)
        else:
            self.bt_send_command.setText("Iniciar Envio")
            self._le_send_frequency.setEnabled(True)
        

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._le_thruster: QLineEdit = QLineEdit("0")
        self._le_top: QLineEdit = QLineEdit("0")
        self._le_right: QLineEdit = QLineEdit("0")
        self._le_bottom: QLineEdit = QLineEdit("0")
        self._le_left: QLineEdit = QLineEdit("0")

        self._le_top_offset: QLineEdit = QLineEdit("0.0")
        self._le_right_offset: QLineEdit = QLineEdit("0.0")
        self._le_bottom_offset: QLineEdit = QLineEdit("0.0")
        self._le_left_offset: QLineEdit = QLineEdit("0.0")

        self._le_send_frequency: QLineEdit = QLineEdit("1.0")

        self._bt_send_commands: QPushButton = QPushButton("Envio Único")
        self._bt_send_offsets: QPushButton = QPushButton("Enviar Offsets")

        self._chb_cycle_send: QCheckBox = QCheckBox("Envio Periódico")

        self._wd_period_parameters: QWidget = QWidget()

        self._send_started: bool = False


        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        lyt_period_parameters: QGridLayout = QGridLayout()
        self._wd_period_parameters.setLayout(lyt_period_parameters)
        lyt_period_parameters.addWidget(QLabel("Frequência de Envio (Hz):"), 0, 0, 1, 1)
        lyt_period_parameters.addWidget(self._le_send_frequency, 0, 1, 1, 1)

        self._wd_period_parameters.setEnabled(False)

        self._layout.addWidget(QLabel("Thruster (-1.0 a 1.0):"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_thruster, 0, 1, 1, 2)

        self._layout.addWidget(QLabel("Top (-45° a 45°):"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_top, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 1, 2, 1, 1)
        self._layout.addWidget(self._le_top_offset, 1, 3, 1, 1)

        self._layout.addWidget(QLabel("Right (-45° a 45°):"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_right, 2, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 2, 2, 1, 1)
        self._layout.addWidget(self._le_right_offset, 2, 3, 1, 1)

        self._layout.addWidget(QLabel("Bottom (-45° a 45°):"), 3, 0, 1, 1)
        self._layout.addWidget(self._le_bottom, 3, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 3, 2, 1, 1)
        self._layout.addWidget(self._le_bottom_offset, 3, 3, 1, 1)
        
        self._layout.addWidget(QLabel("Left (-45° a 45°):"), 4, 0, 1, 1)
        self._layout.addWidget(self._le_left, 4, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 4, 2, 1, 1)
        self._layout.addWidget(self._le_left_offset, 4, 3, 1, 1)

        self._layout.addWidget(self._bt_send_offsets, 5, 0, 1, 4)

        self._layout.addWidget(self._chb_cycle_send, 6, 0, 1, 1)
        self._layout.addWidget(self._wd_period_parameters, 6, 1, 1, 3)

        self._layout.addWidget(self._bt_send_commands, 7, 0, 1, 4)

    def __init_backend__(self):
        self._chb_cycle_send.stateChanged.connect(self.__change_send_mode_callback__)

    def __change_send_mode_callback__(self):
        self._wd_period_parameters.setEnabled(self.periodic_send)
        self.send_started = self._send_started

        if not self.periodic_send:
            self.bt_send_command.setText("Envio Único")

    def serialize(self) -> dict:
        return {
            "top_offset": self.top_offset,
            "right_offset": self.right_offset,
            "bottom_offset": self.bottom_offset,
            "left_offset": self.left_offset,
        }
    
    def deserialize(self, parameters: dict):
        key_widget: dict = {
            "top_offset": self._le_top_offset,
            "right_offset": self._le_right_offset,
            "bottom_offset": self._le_bottom_offset,
            "left_offset": self._le_left_offset
        }
    
        for key in parameters.keys():
            if key in key_widget.keys():
                key_widget[key].setText(str(parameters[key]))
        
