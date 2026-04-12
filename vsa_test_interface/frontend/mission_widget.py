from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QCheckBox, QTabWidget, QPushButton
from .manual_mission_widget import ManualMissionWidget
from .autonomous_mission_widget import AutonomousMissionWidget


class MissionWidget(QGroupBox):
    @property
    def is_autonomous_mission(self) -> bool:
        return self._chb_autonomous_mission.isChecked()

    @property
    def bt_send_mission_parameters(self) -> QPushButton:
        return self._bt_send_mission_parameters
    
    @property
    def manual_mission_widget(self) -> ManualMissionWidget:
        return self._manual_mission
    
    @property
    def autonomous_mission_widget(self) -> AutonomousMissionWidget:
        return self._autonomous_mission

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._chb_autonomous_mission: QCheckBox = QCheckBox("Missão Autônoma")
        self._chb_autonomous_mission.setChecked(True)

        self._tab_missions: QTabWidget = QTabWidget()
        self._bt_send_mission_parameters: QPushButton = QPushButton("Iniciar Missão")

        self._manual_mission: ManualMissionWidget = ManualMissionWidget()
        self._autonomous_mission: AutonomousMissionWidget = AutonomousMissionWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self.setTitle("Missão:")

        self._tab_missions.tabBar().setHidden(True)
        # self._tab_missions.addTab(self._manual_mission, "Manual")
        self._tab_missions.addTab(self._autonomous_mission, "Automatico")

        # self._layout.addWidget(self._chb_autonomous_mission, 0, 0, 1, 1)
        self._layout.addWidget(self._tab_missions, 0, 0, 1, 1)
        self._layout.addWidget(self._bt_send_mission_parameters, 1, 0, 1, 1)

    def __init_backend__(self):
        self._chb_autonomous_mission.stateChanged.connect(self.__chb_autonomous_mission_check_callback__)
        self._bt_send_mission_parameters.clicked.connect(self.__bt_send_mission_parameters_clicked_callback__)

    def __chb_autonomous_mission_check_callback__(self):
        manual: bool = not self._chb_autonomous_mission.isChecked()

        if manual:
            self._tab_missions.setCurrentIndex(0)
            self._bt_send_mission_parameters.setText("Enviar Comandos")
        else:
            self._tab_missions.setCurrentIndex(1)
            self._bt_send_mission_parameters.setText("Iniciar Missão")

    def __bt_send_mission_parameters_clicked_callback__(self):
        manual: bool = not self._chb_autonomous_mission.isChecked()
        print("botao")
