from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QCheckBox, QTabWidget, QPushButton
from .actuators_test_widget import ActuatorsTestWidget
from .payloads_test_widget import PayloadTestWidget
from .autonomous_mission_widget import AutonomousMissionWidget
from .actuators_can_test_widget import ActuatorsCANTestWidget


class MissionWidget(QGroupBox):
    @property
    def is_autonomous_mission(self) -> bool:
        return self._chb_autonomous_mission.isChecked()

    @property
    def bt_send_mission_parameters(self) -> QPushButton:
        return self._autonomous_mission.bt_send_mission_parameters

    @property
    def bt_abort(self) -> QPushButton:
        return self._autonomous_mission.bt_abort
    
    @property
    def actuators_test_widget(self) -> ActuatorsTestWidget:
        return self._actuators_test
    
    @property
    def autonomous_mission_widget(self) -> AutonomousMissionWidget:
        return self._autonomous_mission

    @property
    def payload_test_widget(self) -> PayloadTestWidget:
        return self._payload_test

    @property
    def actuators_can_test_widget(self) -> ActuatorsCANTestWidget:
        return self._actuators_can_test

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._chb_autonomous_mission: QCheckBox = QCheckBox("Missão Autônoma")
        self._chb_autonomous_mission.setChecked(True)

        self._tab_missions: QTabWidget = QTabWidget()
        self._bt_send_mission_parameters: QPushButton = QPushButton("Iniciar Missão")

        self._actuators_test: ActuatorsTestWidget = ActuatorsTestWidget()
        self._actuators_can_test: ActuatorsCANTestWidget = ActuatorsCANTestWidget()
        self._payload_test: PayloadTestWidget = PayloadTestWidget()
        self._autonomous_mission: AutonomousMissionWidget = AutonomousMissionWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        self._tab_missions.addTab(self._autonomous_mission, "Automatico")
        self._tab_missions.addTab(self._actuators_test, "Atuadores")
        self._tab_missions.addTab(self._payload_test, "Leds e Relés")
        self._tab_missions.addTab(self._actuators_can_test, "Atuadores (CAN)")

        # self._layout.addWidget(self._chb_autonomous_mission, 0, 0, 1, 1)
        self._layout.addWidget(self._tab_missions, 0, 0, 1, 1)

    def __init_backend__(self):
        pass

    def serialize(self) -> dict:
        return {

        }

    def deserialize(self, parameters: dict):
        pass
