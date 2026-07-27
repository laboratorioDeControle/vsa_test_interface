from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QCheckBox, QTabWidget, QPushButton
from .calib_measurement_table_widget import CalibMeasurementTableWidget
from .counter_time_widget import CounterTimeWidget
from .calib_results_widget import CalibResultsWidget


class CalibThrusterWidget(QWidget):
    @property
    def bt_start_stop_experiment(self) -> QPushButton:
        return self._bt_start_stop_experiment

    @property
    def bt_calculate(self) -> QPushButton:
        return self._bt_calculate

    @property
    def experiment_parameters(self) -> dict:
        return self._table.experiment_parameters

    @property
    def execution_experiment(self) -> bool:
        return self._execution_experiment

    @execution_experiment.setter
    def execution_experiment(self, value: bool):
        self._execution_experiment = value

        if value:
            self._bt_start_stop_experiment.setText("Parar Thruster")
        else:
            self._bt_start_stop_experiment.setText("Rotacionar Thruster")

    @property
    def counter(self) -> CounterTimeWidget:
        return self._counter

    @property
    def measurement_table(self) -> CalibMeasurementTableWidget:
        return self._table

    @property
    def result(self) -> CalibResultsWidget:
        return self._result

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._table: CalibMeasurementTableWidget = CalibMeasurementTableWidget()
        self._counter: CounterTimeWidget = CounterTimeWidget("Cronômetro")
        self._result: CalibResultsWidget = CalibResultsWidget()

        self._bt_start_stop_experiment: QPushButton = QPushButton("Rotacionar Thruster")
        self._bt_calculate: QPushButton = QPushButton("Calcular Calibração")

        self._layout: QGridLayout = QGridLayout()
        self._execution_experiment: bool = False

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        self._layout.addWidget(self._result, 0, 0, 1, 1)
        self._layout.addWidget(self._counter, 0, 1, 1, 1)
        self._layout.addWidget(self._table, 1, 0, 1, 2)
        self._layout.addWidget(self._bt_start_stop_experiment, 2, 0, 1, 1)
        self._layout.addWidget(self._bt_calculate, 2, 1, 1, 1)

    def __init_backend__(self):
        pass

    def serialize(self) -> dict:
        return {
            "table": self._table.serialize(),
            "result": self._result.serialize()
        }

    def deserialize(self, parameters: dict):
        if "table" in parameters.keys():
            self._table.deserialize(parameters["table"])

        if "result" in parameters.keys():
            self._result.deserialize(parameters["result"])
