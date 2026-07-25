from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QLineEdit, QCheckBox, QPushButton



class PayloadTestWidget(QGroupBox):
    @property
    def bt_send_command(self) -> QPushButton:
        return self._bt_send_commands

    @property
    def relay_1(self) -> QCheckBox:
        return self._chb_relay_1

    @property
    def relay_2(self) -> QCheckBox:
        return self._chb_relay_2

    @property
    def relay_3(self) -> QCheckBox:
        return self._chb_relay_3

    @property
    def relays_msg(self) -> list:
        relay_1: int = int(self._chb_relay_1.isChecked())
        relay_2: int = int(self._chb_relay_2.isChecked())
        relay_3: int = int(self._chb_relay_3.isChecked())

        result: list = [
            0x03,
            relay_1,
            relay_2,
            relay_3,
            1,
            1,
            1
        ]

        return result

    @property
    def red(self) -> int:
        result: int = 0

        try:
            result = int(self._le_red.text())
            if result <= 0:
                result = 0
            elif result >= 255:
                result = 255

        except ValueError:
            pass

        finally:
            self._le_red.setText(str(result))
            return result

    @property
    def green(self) -> int:
        result: int = 0

        try:
            result = int(self._le_green.text())
            if result <= 0:
                result = 0
            elif result >= 255:
                result = 255

        except ValueError:
            pass

        finally:
            self._le_green.setText(str(result))
            return result

    @property
    def blue(self) -> int:
        result: int = 0

        try:
            result = int(self._le_blue.text())
            if result <= 0:
                result = 0
            elif result >= 255:
                result = 255

        except ValueError:
            pass

        finally:
            self._le_blue.setText(str(result))
            return result

    @property
    def white(self) -> int:
        result: int = 0

        try:
            result = int(self._le_white.text())
            if result <= 0:
                result = 0
            elif result >= 255:
                result = 255

        except ValueError:
            pass

        finally:
            self._le_white.setText(str(result))
            return result


    @property
    def leds_msg(self) -> list:

        result: list = [
            0x04,
            self.red,
            self.green,
            self.blue,
            self.white
        ]

        return result

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._layout: QGridLayout = QGridLayout()

        self._le_red: QLineEdit = QLineEdit("0")
        self._le_green: QLineEdit = QLineEdit("0")
        self._le_blue: QLineEdit = QLineEdit("0")
        self._le_white: QLineEdit = QLineEdit("0")

        self._chb_relay_1: QCheckBox = QCheckBox("Relé 1")
        self._chb_relay_2: QCheckBox = QCheckBox("Relé 2")
        self._chb_relay_3: QCheckBox = QCheckBox("Relé 3")

        self._bt_send_commands: QPushButton = QPushButton("Enviar Comando")

        self.__init_ui__()
        self.__init_backend__()

    def __init_ui__(self):
        self.setLayout(self._layout)

        gb_relays: QGroupBox = QGroupBox("Relés:")
        lyt_relays: QGridLayout = QGridLayout()
        gb_relays.setLayout(lyt_relays)

        lyt_relays.addWidget(self._chb_relay_1, 0, 0, 1, 1)
        lyt_relays.addWidget(self._chb_relay_2, 1, 0, 1, 1)
        lyt_relays.addWidget(self._chb_relay_3, 2, 0, 1, 1)

        gb_leds: QGroupBox = QGroupBox("Leds:")
        lyt_leds: QGridLayout = QGridLayout()
        gb_leds.setLayout(lyt_leds)

        lyt_leds.addWidget(QLabel("Vermelho (0-255):"), 0, 0, 1, 1)
        lyt_leds.addWidget(QLabel("Verde (0-255):"), 1, 0, 1, 1)
        lyt_leds.addWidget(QLabel("Azul (0-255):"), 2, 0, 1, 1)
        lyt_leds.addWidget(QLabel("Branco (0-255):"), 3, 0, 1, 1)
        lyt_leds.addWidget(self._le_red, 0, 1, 1, 1)
        lyt_leds.addWidget(self._le_green, 1, 1, 1, 1)
        lyt_leds.addWidget(self._le_blue, 2, 1, 1, 1)
        lyt_leds.addWidget(self._le_white, 3, 1, 1, 1)
        lyt_leds.addWidget(self._bt_send_commands, 4, 0, 1, 2)

        self._layout.addWidget(gb_leds, 0, 0, 1, 1)
        self._layout.addWidget(gb_relays, 1, 0, 1, 1)

    def __init_backend__(self):
        pass
