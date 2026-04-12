from PyQt5.QtWidgets import QWidget, QGridLayout
from .com_topics_widget import ComTopicsWidget
from .live_plot_widget import LivePlotWidget
from .mission_widget import MissionWidget


class IHMMainWidget(QWidget):
    @property
    def com_topics(self) -> ComTopicsWidget:
        return self._com_topics
    
    @property
    def mission(self) -> MissionWidget:
        return self._mission

    @property
    def speed_graph(self) -> LivePlotWidget:
        return self._speed_graph
    
    @property
    def xy_graph(self) -> LivePlotWidget:
        return self._xy_graph

    def __init__(self, parent : QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()
        self._com_topics: ComTopicsWidget = ComTopicsWidget()

        self._speed_graph: LivePlotWidget = LivePlotWidget("Velocidade(x,y) x Tempo", "Velocidade", "m/s", "tempo", "s", offset_button=False,
                                                            use_header_name=False, sample_time_seconds=1.0)
        
        self._xy_graph: LivePlotWidget = LivePlotWidget("Posição no Plano x,y", "Posição X", "m", "Posição Y", "m", offset_button=False,
                                                            use_header_name=False, sample_time_seconds=1.0)
        
        self._mission: MissionWidget = MissionWidget()

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)
        self._layout.addWidget(self._com_topics, 0, 0, 1, 1)
        self._layout.addWidget(self._mission, 0, 1, 1, 1)
        self._layout.addWidget(self._speed_graph, 1, 0, 1, 1)
        self._layout.addWidget(self._xy_graph, 1, 1, 1, 1)

    def __init_backend__(self):
        pass