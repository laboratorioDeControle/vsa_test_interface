from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QGroupBox, QPushButton


class ComTopicsWidget(QGroupBox):
    @property
    def odometry_topic(self) -> str:
        return self._le_odometry_topic.text()
    
    @property
    def thruster_topic(self) -> str:
        return self._le_thruster_input_topic.text()
    
    @property
    def rudders_topic(self) -> str:
        return self._le_rudders_input_topic.text()
    
    @property
    def heart_beat_topic(self) -> str:
        return self._le_heart_beat_topic.text()

    @property
    def bt_start_sampling(self) -> QPushButton:
        return self._bt_start_sampling

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()

        self._le_odometry_topic: QLineEdit = QLineEdit("/lauv/dynamics/odometry")
        self._le_thruster_input_topic: QLineEdit = QLineEdit("/lauv/controller/thrusters_setpoints")
        self._le_rudders_input_topic: QLineEdit = QLineEdit("/lauv/controller/rudders_setpoints")
        self._le_heart_beat_topic: QLineEdit = QLineEdit("/imc_heartbeat")

        self._bt_start_sampling: QPushButton = QPushButton("Iniciar Comunicação")

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self.setTitle("Tópicos:")

        self._layout.addWidget(QLabel("Odometria:"), 0, 0, 1, 1)
        self._layout.addWidget(self._le_odometry_topic, 0, 1, 1, 1)
        self._layout.addWidget(QLabel("Thruster:"), 1, 0, 1, 1)
        self._layout.addWidget(self._le_thruster_input_topic, 1, 1, 1, 1)
        self._layout.addWidget(QLabel("Lemes:"), 2, 0, 1, 1)
        self._layout.addWidget(self._le_rudders_input_topic, 2, 1, 1, 1)
        self._layout.addWidget(QLabel("Heart Beat:"), 3, 0, 1, 1)
        self._layout.addWidget(self._le_heart_beat_topic, 3, 1, 1, 1)

        self._layout.addWidget(self._bt_start_sampling, 4, 0, 1, 2)

    def __init_backend__(self):
        pass

    def start_stop_comunication(self, start_stop: bool):
        self._le_odometry_topic.setEnabled(not start_stop)
        self._le_thruster_input_topic.setEnabled(not start_stop)
        self._le_rudders_input_topic.setEnabled(not start_stop)
        self._le_heart_beat_topic.setEnabled(not start_stop)

        bt_text: str = "Iniciar Comunicação"
        
        if start_stop:
            bt_text = "Encerrar Comunicação"

        self._bt_start_sampling.setText(bt_text)
