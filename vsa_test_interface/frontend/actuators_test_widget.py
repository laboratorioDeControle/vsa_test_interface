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
    def servo_1(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_servo_1.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_servo_1.setText(str(result))
            return result

    @property
    def servo_2(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_servo_2.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_servo_2.setText(str(result))
            return result

    @property
    def servo_3(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_servo_3.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_servo_3.setText(str(result))
            return result

    @property
    def servo_4(self) -> float:
        result: float = 0.0

        try:
            result = float(self._le_servo_4.text())
            if result < -45.0:
                result = -45.0
            elif result > 45.0:
                result = 45.0

        except ValueError:
            pass

        finally:
            self._le_servo_4.setText(str(result))
            return result

    @property
    def servo_down_offset(self) -> float:
        """Offset for servo 1 (top) in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_servo_1_offset.text())
        except ValueError:
            pass
        finally:
            self._le_servo_1_offset.setText(str(result))
            return result

    @property
    def servo_up_offset(self) -> float:
        """Offset for servo 2 (right) in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_servo_2_offset.text())
        except ValueError:
            pass
        finally:
            self._le_servo_2_offset.setText(str(result))
            return result

    @property
    def servo_left_offset(self) -> float:
        """Offset for servo 3 (down) in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_servo_3_offset.text())
        except ValueError:
            pass
        finally:
            self._le_servo_3_offset.setText(str(result))
            return result

    @property
    def servo_right_offset(self) -> float:
        """Offset for servo 4 (left) in degrees"""
        result: float = 0.0
        try:
            result = float(self._le_servo_4_offset.text())
        except ValueError:
            pass
        finally:
            self._le_servo_4_offset.setText(str(result))
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
            math.radians(self.servo_1),
            math.radians(self.servo_2),
            math.radians(self.servo_3),
            math.radians(self.servo_4)
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
        self._le_servo_1: QLineEdit = QLineEdit("0")
        self._le_servo_2: QLineEdit = QLineEdit("0")
        self._le_servo_3: QLineEdit = QLineEdit("0")
        self._le_servo_4: QLineEdit = QLineEdit("0")

        self._le_servo_1_offset: QLineEdit = QLineEdit("0.0")
        self._le_servo_2_offset: QLineEdit = QLineEdit("0.0")
        self._le_servo_3_offset: QLineEdit = QLineEdit("0.0")
        self._le_servo_4_offset: QLineEdit = QLineEdit("0.0")

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

        self._layout.addWidget(QLabel("Servo 1 (Top) (-45° a 45°):"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_servo_1, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 1, 2, 1, 1)
        self._layout.addWidget(self._le_servo_1_offset, 1, 3, 1, 1)

        self._layout.addWidget(QLabel("Servo 2 (Right) (-45° a 45°):"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_servo_2, 2, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 2, 2, 1, 1)
        self._layout.addWidget(self._le_servo_2_offset, 2, 3, 1, 1)

        self._layout.addWidget(QLabel("Servo 3 (Down) (-45° a 45°):"), 3, 0, 1, 1)
        self._layout.addWidget(self._le_servo_3, 3, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 3, 2, 1, 1)
        self._layout.addWidget(self._le_servo_3_offset, 3, 3, 1, 1)
        
        self._layout.addWidget(QLabel("Servo 4 (Left) (-45° a 45°):"), 4, 0, 1, 1)
        self._layout.addWidget(self._le_servo_4, 4, 1, 1, 1)
        self._layout.addWidget(QLabel("Offset (°):"), 4, 2, 1, 1)
        self._layout.addWidget(self._le_servo_4_offset, 4, 3, 1, 1)

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
