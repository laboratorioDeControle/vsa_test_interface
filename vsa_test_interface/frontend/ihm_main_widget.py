from PyQt5.QtWidgets import QWidget, QGridLayout, QTabWidget
from .com_topics_widget import ComTopicsWidget
from .widgets.live_plot_widget import LivePlotWidget
from .widgets.bus_msg_log_widget import BusMsgLogWidget
from .mission_widget import MissionWidget
from .calibration_widget import CalibrationWidget


class IHMMainWidget(QWidget):
    @property
    def com_topics(self) -> ComTopicsWidget:
        return self._com_topics
    
    @property
    def mission(self) -> MissionWidget:
        return self._mission

    @property
    def calibration(self) -> CalibrationWidget:
        return self._calibration

    @property
    def speed_graph(self) -> LivePlotWidget:
        return self._speed_graph
    
    @property
    def xy_graph(self) -> LivePlotWidget:
        return self._xy_graph

    @property
    def log(self) -> BusMsgLogWidget:
        return self._msg_log

    def __init__(self, parent : QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()
        self._com_topics: ComTopicsWidget = ComTopicsWidget()

        self._speed_graph: LivePlotWidget = LivePlotWidget("Velocidade(x,y) x Tempo", "Velocidade", "m/s", "tempo", "s", offset_button=False,
                                                            use_header_name=False, sample_time_seconds=1.0)
        
        self._xy_graph: LivePlotWidget = LivePlotWidget("Posição no Plano x,y", "Posição X", "m", "Posição Y", "m", offset_button=False,
                                                            use_header_name=False, sample_time_seconds=1.0)

        self._msg_log: BusMsgLogWidget = BusMsgLogWidget()
        
        self._mission: MissionWidget = MissionWidget()
        self._calibration: CalibrationWidget = CalibrationWidget()

        self._tab: QTabWidget = QTabWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        self._tab.addTab(self._calibration, "Calibração")
        self._tab.addTab(self._mission, "Modo de Operação")

        self._layout.addWidget(self._com_topics, 0, 0, 1, 1)
        self._layout.addWidget(self._tab, 0, 1, 3, 1)
        self._layout.addWidget(self._speed_graph, 1, 0, 2, 1)
        # self._layout.addWidget(self._xy_graph, 1, 1, 1, 1)

    def __init_backend__(self):
        pass

    def serialize(self) -> dict:
        return {
            "com_topics": self.com_topics.serialize(),
            "calibration": self.calibration.serialize()
        }

    def deserialize(self, parameters: dict):
        if "com_topics" in parameters.keys():
            self.com_topics.deserialize(parameters["com_topics"])

        if "calibration" in parameters.keys():
            self.calibration.deserialize(parameters["calibration"])
            thruster_calib: list = self.calibration.calib_thruster.result.poly_coef
            self.mission.autonomous_mission_widget.thruster_calib = thruster_calib
