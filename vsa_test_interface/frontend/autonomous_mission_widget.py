from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit, QPushButton, QCheckBox
from .widgets.autonomous_mission_actuators_widget import AutonomousMissionActuatorsWidget
from ..backend.tools import deg2rad, rad2deg, json_to_dict, dict_to_json
from ..frontend.resources import open_file_dialog, save_file_dialog


class AutonomousMissionWidget(QGroupBox):
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

    @cycle_frequency.setter
    def cycle_frequency(self, value: float):
        self._le_cycle_frequency.setText(str(value))

    @property
    def complete_oscilation(self) -> int:
        return int(self._chb_complete_oscilation.isChecked())

    @complete_oscilation.setter
    def complete_oscilation(self, value: int):
        self._chb_complete_oscilation.setChecked(value != 0)

    @property
    def bt_send_mission_parameters(self) -> QPushButton:
        return self._bt_send_mission

    @property
    def bt_abort(self) -> QPushButton:
        return self._bt_abort

    @property
    def mission_parameters(self) -> dict:
        return {
            "pre_dive_time": self._pre_dive_widget.step_time,
            "pre_dive_start_delay": self._pre_dive_widget.delay_time,
            "pre_dive_thruster_power": self._pre_dive_widget.thruster_power,
            "pre_dive_vertical_rudders_angle": deg2rad(self._pre_dive_widget.vertical_rudders_angle),
            "pre_dive_horizontal_rudders_angle": deg2rad(self._pre_dive_widget.horizontal_rudders_angle),

            "dive_time": self._dive_widget.step_time,
            "dive_start_delay": self._dive_widget.delay_time,
            "dive_thruster_power": self._dive_widget.thruster_power,
            "dive_vertical_rudders_angle": deg2rad(self._dive_widget.vertical_rudders_angle),
            "dive_horizontal_rudders_angle": deg2rad(self._dive_widget.horizontal_rudders_angle),
            "dive_cycle_frequency": self.cycle_frequency,
            "dive_complete_oscilation": self.complete_oscilation
        }

    @mission_parameters.setter
    def mission_parameters(self, value: dict):
        self._pre_dive_widget.step_time = value.get("pre_dive_time", 1.0)
        self._pre_dive_widget.delay_time = value.get("pre_dive_start_delay", 1.0)
        self._pre_dive_widget.thruster_power = value.get("pre_dive_thruster_power", 0.0) * 100.0
        self._pre_dive_widget.vertical_rudders_angle = rad2deg(value.get("pre_dive_vertical_rudders_angle", 0.0))
        self._pre_dive_widget.horizontal_rudders_angle = rad2deg(value.get("pre_dive_horizontal_rudders_angle", 0.0))

        self._dive_widget.step_time = value.get("dive_time", 1.0)
        self._dive_widget.delay_time = value.get("dive_start_delay", 1.0)
        self._dive_widget.thruster_power = value.get("dive_thruster_power", 0.0) * 100.0
        self._dive_widget.vertical_rudders_angle = rad2deg(value.get("dive_vertical_rudders_angle", 0.0))
        self._dive_widget.horizontal_rudders_angle = rad2deg(value.get("dive_horizontal_rudders_angle", 0.0))
        self.cycle_frequency = value.get("dive_cycle_frequency", 1.0)
        self.complete_oscilation = value.get("dive_complete_oscilation", 0)
        

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._pre_dive_widget: AutonomousMissionActuatorsWidget = AutonomousMissionActuatorsWidget("1 - Pré-Mergulho")
        self._dive_widget: AutonomousMissionActuatorsWidget = AutonomousMissionActuatorsWidget("2 - Mergulho")

        self._le_cycle_frequency: QLineEdit = QLineEdit("1.0")
        self._chb_complete_oscilation: QCheckBox = QCheckBox("Oscilação Completa")

        self._bt_send_mission: QPushButton = QPushButton("Enviar Missão")
        self._bt_abort: QPushButton = QPushButton("Abortar")
        self._bt_export: QPushButton = QPushButton("Exportar Missão")
        self._bt_import: QPushButton = QPushButton("Importar Missão")

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        self._layout.addWidget(self._pre_dive_widget, 0, 0, 1, 2)
        self._layout.addWidget(self._dive_widget, 1, 0, 1, 2)
        
        self._dive_widget.main_layout.addWidget(QLabel("Frequência das Oscilações:"), 5, 0, 1, 1)
        self._dive_widget.main_layout.addWidget(self._le_cycle_frequency, 5, 1, 1, 1)
        self._dive_widget.main_layout.addWidget(QLabel("Hz"), 5, 2, 1, 1)
        self._dive_widget.main_layout.addWidget(self._chb_complete_oscilation, 6, 0, 1, 2)

        self._layout.addWidget(self._bt_send_mission, 2, 0, 1, 1)
        self._layout.addWidget(self._bt_abort, 2, 1, 1, 1)
        self._layout.addWidget(self._bt_import, 3, 0, 1, 1)
        self._layout.addWidget(self._bt_export, 3, 1, 1, 1)

    def set_thruster_calib(self, calib: list):
        self._dive_widget.thruster_calib = calib
        self._pre_dive_widget.thruster_calib = calib

    def __init_backend__(self):
        self._bt_export.clicked.connect(self.__bt_export_callback__)
        self._bt_import.clicked.connect(self.__bt_import_callback__)

    def __bt_import_callback__(self):
        file_path: str = open_file_dialog(self,
                                          "Arquivo de Missão",
                                          "Parâmetros para Missão",
                                          ".json")

        if file_path != "":
            imported: dict = json_to_dict(file_path)
            self.mission_parameters = imported

    def __bt_export_callback__(self):
        file_path: str = save_file_dialog(self,
                                          "Arquivo de Missão",
                                          "Parâmetros para Missão",
                                          ".json")

        if file_path != "":
            dict_to_json(file_path, self.mission_parameters)
