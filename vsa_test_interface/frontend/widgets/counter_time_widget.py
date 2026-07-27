from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import QTimer


class CounterTimeWidget(QGroupBox):
    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value: bool):
        self._running = value
        if self._running:
            self._bt_start_stop.setText("Parar")
        else:
            self._bt_start_stop.setText("Iniciar")

    @property
    def elapsed_seconds(self) -> int:
        return self._output_seconds

    def __init__(self, title: str = "Tempo", show_control: bool = False, parent: QWidget = None):
        super().__init__(parent)

        self._title: str = title
        self._show_control: bool = show_control

        self._hour: int = 0
        self._minute: int = 0
        self._second: int = 0

        self._running: bool = False

        self._layout: QGridLayout = QGridLayout()
        self._lbl_counter: QLabel = QLabel("00:00:00")

        self._bt_start_stop: QPushButton = QPushButton("Iniciar")
        self._bt_reset: QPushButton = QPushButton("Reiniciar")

        self._timer: QTimer = QTimer()
        self._output_seconds: int = 0

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setTitle(self._title + ":")
        self.setLayout(self._layout)

        self._lbl_counter.setStyleSheet("font-size: 24pt;")
        self._layout.addWidget(self._lbl_counter, 0, 0, 1, 2)
        self._layout.addWidget(self._bt_start_stop, 1, 0, 1, 1)
        self._layout.addWidget(self._bt_reset, 1, 1, 1, 1)

        self._bt_start_stop.setVisible(self._show_control)
        self._bt_reset.setVisible(self._show_control)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

    def __init_backend__(self):
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.__timer_callback__)

        self._bt_start_stop.clicked.connect(self.__bt_start_stop_callback__)
        self._bt_reset.clicked.connect(self.zero)

    def __format_time__(self) -> str:
        result: str = ""

        hour_text: str = str(self._hour) + ":"
        if self._hour < 10:
            hour_text = "0" + hour_text

        minute_text: str = str(self._minute) + ":"
        if self._minute < 10:
            minute_text = "0" + minute_text

        second_text: str = str(self._second)
        if self._second < 10:
            second_text = "0" + second_text

        result = hour_text + minute_text + second_text
        return result

    def __bt_start_stop_callback__(self):
        self.running = not self.running

        if self.running:
            self.start()
        else:
            self.stop()

    def __timer_callback__(self):
        self._output_seconds += 1
        self._second += 1

        if self._second == 60:
            self._second = 0
            self._minute += 1

            if self._minute == 60:
                self._minute = 0
                self._hour += 1

        self._lbl_counter.setText(self.__format_time__())

    def zero(self):
        self.stop()
        self._hour = 0
        self._minute = 0
        self._second = 0
        self._output_seconds = 0

        self._lbl_counter.setText(self.__format_time__())

    def stop(self):
        self._timer.stop()
        self.running = False

    def start(self):
        self._timer.start()
        self.running = True
