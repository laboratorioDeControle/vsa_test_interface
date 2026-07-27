from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy
from ...backend.tools import json_to_dict, dict_to_json
from ...frontend.resources import open_file_dialog, save_file_dialog


class CalibMeasurementTableWidget(QGroupBox):
    @property
    def experiment_parameters(self) -> dict:
        result: dict = {
            "power": self.power,
            "distance": self.distance,
            "time": self.time
        }
        return result

    @property
    def power(self) -> float | None:
        selected_items: list = self._table.selectedItems()

        if len(selected_items) > 0:
            power: float = 0.0
            item: QTableWidgetItem = selected_items[0]
            row: int = item.row()

            try:
                power = float(self._table.item(row, 0).text())

                if power > 100.0:
                    power = 100.0
                elif power < -100.0:
                    power = -100.0
            except:
                pass
            finally:
                self._table.item(row, 0).setText(str(power))
                return power

        return None

    @property
    def distance(self) -> float | None:
        selected_items: list = self._table.selectedItems()

        if len(selected_items) > 0:
            distance: float = 0.0
            item: QTableWidgetItem = selected_items[0]
            row: int = item.row()

            try:
                distance = float(self._table.item(row, 1).text())

                if distance < 0.0:
                    distance = 0.0
            except:
                pass
            finally:
                self._table.item(row, 1).setText(str(distance))
                return distance

        return None

    @property
    def time(self) -> float | None:
        selected_items: list = self._table.selectedItems()

        if len(selected_items) > 0:
            time: float = 0.0
            item: QTableWidgetItem = selected_items[0]
            row: int = item.row()

            try:
                time = float(self._table.item(row, 2).text())

                if time < 0.0:
                    time = 0.0
            except:
                pass
            finally:
                self._table.item(row, 2).setText(str(time))
                return time

        return None

    @time.setter
    def time(self, value: float):
        selected_items: list = self._table.selectedItems()
        if len(selected_items) > 0:
            item: QTableWidgetItem = selected_items[0]
            row: int = item.row()
            self._table.item(row, 2).setText(str(value))

            if value != 0.0:
                distance: float = self.distance
                speed: float = distance / value
                self._table.item(row, 3).setText(str(speed))
        

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._layout: QGridLayout = QGridLayout()

        self._table: QTableWidget = QTableWidget()
        self._bt_add: QPushButton = QPushButton("Adicionar")
        self._bt_remove: QPushButton = QPushButton("Remover")

        self._bt_export: QPushButton = QPushButton("Exportar")
        self._bt_import: QPushButton = QPushButton("Importar")

        self._headers: list = ["Potência (%)", "Distância (m)", "Tempo (s)", "Velocidade Média (m/s)"]

        self.__init_ui__()
        self.__init_backend__()
        self.__initialize_table__()

    def __init_ui__(self):
        self.setTitle("Tabela de Medidas:")
        self.setLayout(self._layout)

        gb_table_operations: QGroupBox = QGroupBox()
        lyt_table_operations: QGridLayout = QGridLayout()
        gb_table_operations.setLayout(lyt_table_operations)
        gb_table_operations.setTitle("Inserir / Remover Medidas:")

        lyt_table_operations.addWidget(self._bt_add, 0, 0, 1, 1)
        lyt_table_operations.addWidget(self._bt_remove, 0, 1, 1, 1)

        gb_export_import_table: QGroupBox = QGroupBox()
        lyt_export_import_table: QGridLayout = QGridLayout()
        gb_export_import_table.setLayout(lyt_export_import_table)
        gb_export_import_table.setTitle("Exportar / Importar Medidas:")
        
        lyt_export_import_table.addWidget(self._bt_import, 0, 0, 1, 1)
        lyt_export_import_table.addWidget(self._bt_export, 0, 1, 1, 1)

        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._layout.addWidget(self._table, 0, 0, 1, 2)
        self._layout.addWidget(gb_table_operations, 1, 0, 1, 2)
        self._layout.addWidget(gb_export_import_table, 2, 0, 1, 2)

        self._table.setColumnCount(len(self._headers))
        self._table.setHorizontalHeaderLabels(self._headers)

    def __init_backend__(self):
        self._bt_add.clicked.connect(self.__bt_add_callback__)
        self._bt_remove.clicked.connect(self.__bt_remove_callback__)
        self._bt_import.clicked.connect(self.__bt_import_table_callback__)
        self._bt_export.clicked.connect(self.__bt_export_table_callback__)

    def __bt_add_callback__(self):
        self._table.insertRow(self._table.rowCount())

        for col in range(self._table.columnCount()):
            item: QTableWidgetItem = QTableWidgetItem("0.0")
            self._table.setItem(self._table.rowCount() - 1, col, item)

    def __bt_remove_callback__(self):
        selected_index: int = -1

        try:
            selected_index = self._table.selectedIndexes()[0].row()
        except IndexError:
            pass

        if self._table.rowCount() > 0 and selected_index != -1:
            self._table.removeRow(selected_index)

    def __bt_import_table_callback__(self):
        file_path: str = open_file_dialog(self,
                                          "Arquivo de Medidas",
                                          "Medidas para Calibração",
                                          ".json")

        if file_path != "":
            imported: dict = json_to_dict(file_path)
            self.deserialize(imported)

    def __bt_export_table_callback__(self):
        file_path: str = save_file_dialog(self,
                                          "Arquivo de Medidas",
                                          "Medidas para Calibração",
                                          ".json")

        if file_path != "":
            dict_to_json(file_path, self.serialize(), output_file_extension="")

    def __initialize_table__(self):
        distance: float = 25.0
        time: float = 0.0
        current_power = 10.0

        while current_power <= 100:
            self.__bt_add_callback__()
            row: int = self._table.rowCount() - 1

            self._table.setItem(row, 0, QTableWidgetItem(str(current_power)))
            self._table.setItem(row, 1, QTableWidgetItem(str(distance)))
            self._table.setItem(row, 2, QTableWidgetItem(str(time)))
            self._table.setItem(row, 3, QTableWidgetItem(str(time)))

            current_power += 10.0

    def get_measurements(self) -> dict:
        result: dict = {}

        for header in self._headers:
            result[header] = []

        for row in range(self._table.rowCount()):
            power: float = float(self._table.item(row, 0).text())
            distance: float = float(self._table.item(row, 1).text())
            time: float = float(self._table.item(row, 2).text())
            speed: float = float(self._table.item(row, 3).text())

            result["Potência (%)"].append(power)
            result["Distância (m)"].append(distance)
            result["Tempo (s)"].append(time)
            result["Velocidade Média (m/s)"].append(speed)

        return result

    def __set_measurements__(self, values: dict):
        while self._table.rowCount() > 0:
            self._table.removeRow(self._table.rowCount() - 1)

        self._table.setColumnCount(len(self._headers))
        self._table.setHorizontalHeaderLabels(self._headers)

        if (("Potência (%)" in values.keys()) 
            and ("Distância (m)" in values.keys())
            and ("Tempo (s)" in values.keys())
            and ("Velocidade Média (m/s)" in values.keys())):

            for row in range(len(values["Tempo (s)"])):
                power: float = values["Potência (%)"][row]
                distance: float = values["Distância (m)"][row]
                time: float = values["Tempo (s)"][row]
                speed: float = values["Velocidade Média (m/s)"][row]

                self.__add_measurement__(power, row, 0)
                self.__add_measurement__(distance, row, 1)
                self.__add_measurement__(time, row, 2)
                self.__add_measurement__(speed, row, 3)
            

    def __add_measurement__(self, measurement: float, row: int, col: int):
        if self._table.rowCount() < (row + 1):
            self._table.insertRow(self._table.rowCount())

        item: QTableWidgetItem = QTableWidgetItem(str(measurement))
        self._table.setItem(row, col, item)

    def update_measurement(self, measurement: float):
        try:
            row: int = self._table.selectedIndexes()[0].row()
            self.__add_measurement__(measurement, row, 1)

        except IndexError:
            pass

    def clear(self):
        while self._table.rowCount() > 0:
            self._table.removeRow(self._table.rowCount() - 1)

    def serialize(self) -> dict:
        return {
            "data": self.get_measurements()
        }

    def deserialize(self, parameters: dict):
        if "data" in parameters.keys():
            self.__set_measurements__(parameters["data"])
