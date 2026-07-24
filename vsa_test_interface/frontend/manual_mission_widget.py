from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit, QPushButton


class ManualMissionWidget(QGroupBox):
    @property
    def bt_send_command(self) -> QPushButton:
        return self._bt_send_commands

    @property
    def motors_msg(self) -> list:
        thruster: int = int(self._le_thruster.text())
        truster_dir: int = int(thruster > 0)

        result: list = [
            0x01,
            int(self._le_servo_1.text()),
            int(self._le_servo_2.text()),
            int(self._le_servo_3.text()),
            int(self._le_servo_4.text()),
            truster_dir,
            int(abs(thruster)),
            0x01

        ]

        return result
        

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._le_thruster: QLineEdit = QLineEdit("0")
        self._le_servo_1: QLineEdit = QLineEdit("0")
        self._le_servo_2: QLineEdit = QLineEdit("0")
        self._le_servo_3: QLineEdit = QLineEdit("0")
        self._le_servo_4: QLineEdit = QLineEdit("0")

        self._bt_send_commands: QPushButton = QPushButton("Enviar Comando")

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self.setTitle("Manual:")

        self._layout.addWidget(QLabel("Thruster (PWM):"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_thruster, 0, 1, 1, 1)

        self._layout.addWidget(QLabel("Servo 1 (PWM):"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_servo_1, 1, 1, 1, 1)

        self._layout.addWidget(QLabel("Servo 2 (PWM):"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_servo_2, 2, 1, 1, 1)

        self._layout.addWidget(QLabel("Servo 3 (PWM):"), 3, 0, 1, 1)
        self._layout.addWidget(self._le_servo_3, 3, 1, 1, 1)
        
        self._layout.addWidget(QLabel("Servo 4 (PWM):"), 4, 0, 1, 1)
        self._layout.addWidget(self._le_servo_4, 4, 1, 1, 1)

        self._layout.addWidget(self._bt_send_commands, 5, 0, 1, 2)

    def __init_backend__(self):
        pass