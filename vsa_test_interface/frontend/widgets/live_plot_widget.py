from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
import pyqtgraph as pg


class LivePlotWidget(QGroupBox):
    @property
    def current_y(self) -> float:
        return self._current_y

    @property
    def current_x(self) -> float:
        return self._current_x

    @property
    def data_x(self) -> list:
        return self._x

    @property
    def data_y(self) -> list:
        return self._y

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def bt_zero(self) -> QPushButton:
        return self._bt_zero

    @property
    def header_name(self) -> str:
        return self._header_name

    @header_name.setter
    def header_name(self, value: str):
        self._header_name = value
        self._le_header_name.setText(value)

    def __init__(self, name: str = "", y_label: str = "", y_unit: str = "",
                 x_label: str = "", x_unit: str = "", prefix: str = "",
                 offset_button: bool = True, use_header_name: bool = False,
                 sample_time_seconds: float = 1.0, num_points: int = 500, parent: QWidget = None):
        super().__init__(parent)

        self._prefix: str = prefix
        self._name: str = name
        self._header_name: str = name.replace(":", "")
        self._y_label: str = y_label
        self._y_unit: str = y_unit
        self._x_label: str = x_label
        self._x_unit: str = x_unit
        self._offset_button: bool = offset_button
        self._use_header_name: bool = use_header_name

        self._x: list = []
        self._y: list = []

        self._sum_x: float = 0.0

        self._current_x: float = 0.0
        self._current_y: float = 0.0

        self._last_sampled_x: float = 0.0
        self._sample_x: float = sample_time_seconds

        self._layout_main: QGridLayout = QGridLayout()

        self._graph: pg.PlotWidget = pg.PlotWidget()
        self._graph_pen = pg.mkPen(width=2, color='w')

        self._plot: pg.PlotWidget = self._graph.plot(self._x, self._y, pen=self._graph_pen)
        self._scatter: pg.ScatterPlotItem = pg.ScatterPlotItem(self._x, self._y, pen=pg.mkPen(width=5, color='r'),
                                                               symbol='o', size=5)

        self._le_current_y: QLabel = QLabel("") # QLabel("%.4f %s" % (self.current_y, self._y_unit))
        self._le_header_name: QLineEdit = QLineEdit(self._header_name)
        self._bt_zero: QPushButton = QPushButton("Zerar")

        self._num_points: int = num_points

        self.__init_graph__()
        self.__init_ui__()
        self.__init_behaviour__()

    def __init_ui__(self) -> None:
        bt_zero_row: int = 0

        self.setTitle(self._name)
        self.setLayout(self._layout_main)

        # self._layout_main.addWidget(QLabel(self._y_label), 0, 0, 1, 1)
        self._layout_main.addWidget(self._le_current_y, 0, 0, 1, 1)

        if self._use_header_name:
            self._layout_main.addWidget(QLabel("Nome no Cabeçalho:"), 1, 0, 1, 1)
            self._layout_main.addWidget(self._le_header_name, 1, 1, 1, 1)
            bt_zero_row = 1

        if self._offset_button:
            self._layout_main.addWidget(self.bt_zero, bt_zero_row, 9, 1, 1)

        self._layout_main.addWidget(self._graph, 2, 0, 10, 10)

    def __init_graph__(self) -> None:
        x_label: str = self._x_label + " (" + self._x_unit + ")"
        if self._x_unit == "":
            x_label = self._x_label

        y_label: str = self._y_label + " (" + self._y_unit + ")"
        if self._y_unit == "":
            y_label = self._y_label

        self._graph.setLabel("left", y_label)
        self._graph.setLabel("bottom", x_label)
        self._graph.showGrid(x=True, y=True)

    def __init_behaviour__(self):
        self._le_header_name.textChanged.connect(self.__le_header_name_edit_callback__)

    def __le_header_name_edit_callback__(self):
        self._header_name = self._le_header_name.text()

    def set_x_label(self, x_label: str, x_unit: str):
        self._x_label = x_label
        self._x_unit = x_unit
        self.__init_graph__()

    def set_y_label(self, y_label: str, y_unit: str):
        self._y_label = y_label
        self._y_unit = y_unit
        self.__init_graph__()

    def plot(self, x: list, y: list, hold_last: bool = False) -> None:
        if not hold_last:
            self.clear()

        self._plot.setData(x, y)
        self._plot.setPos(0, 0)

        if len(x) > 0:
            self._current_x = x[len(x) - 1]

        if len(y) > 0:
            self._current_y = y[len(y) - 1]

        self.update()

    def plot_scatter(self, x: list, y: list, hold_last: bool = False) -> None:
        if not hold_last:
            self.clear()

        self._scatter.setData(x, y)

        if len(x) > 0:
            self._current_x = x[len(x) - 1]

        if len(y) > 0:
            self._current_y = y[len(y) - 1]

        self._graph.addItem(self._scatter)

        self.update()

    def live_plot(self, x: float = 0.0, y: float = 0.0, x_is_dx: bool = False, force_dx: float = -1.0) -> None:
        time_to_sample: bool = False

        if x_is_dx:
            self._sum_x += x
            dx: float = self._sum_x - self._last_sampled_x

            if dx >= self._sample_x:
                time_to_sample = True
                self._last_sampled_x = self._sum_x
        else:
            if force_dx != -1.0:
                self._sum_x += force_dx
                dx: float = self._sum_x - self._last_sampled_x

                if dx >= self._sample_x:
                    time_to_sample = True
                    self._last_sampled_x = self._sum_x
            
            else:
                self._sum_x = x
                time_to_sample = True

        if time_to_sample:
            # if len(self._x) >= self._num_points:
            #    self._x.pop(0)
            #    self._y.pop(0)

            self._x.append(self._sum_x)
            self._y.append(y)

            self._plot.setData(self._x, self._y)
            # self._plot.setPos(x, 0)

            self._current_x = x
            self._current_y = y

        self.update()

    def force_last_value_label(self, force_text: str):
        self._le_current_y.setText(force_text)
        self.update()

    def clear(self):
        self._graph.clear()
        self._x = []
        self._y = []
        self._sum_x = 0.0
        self._last_sampled_x = 0.0
        self._current_y = 0.0
        self._plot = self._graph.plot(self._x, self._y, pen=self._graph_pen)
        self._scatter = pg.ScatterPlotItem(self._x, self._y, pen=pg.mkPen(width=5, color='r'),
                                           symbol='o', size=5)

        self.update()

    def update(self):
        super().update()
        self._le_current_y.setText("%.4f %s" % (self.current_y, self._y_unit))