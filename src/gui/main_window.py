from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer
import threading
from tsp_genetic import TSPGenetic
from gui.settings_widget import SettingsWidget
from gui.map_widget import MapWidget
from gui.evolution_widget import EvolutionWidget
from utils import PARAMS
import numpy
import json

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._window = QMainWindow()
        self._window.setWindowTitle("TSP Genetic Algorithm")
        self._window.move(100, 100)
        self._window.setCentralWidget(self)

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)
        self.execution_queue = []
        self.tsp_genetic = None
        self.show_evolution = False
        self.close_tsp = False

        self._window.show()

    def initUI(self):
        self.setLayout(QHBoxLayout())

        self.settings = SettingsWidget(self)
        self.map = MapWidget(self)
        self.evolution = EvolutionWidget(self)
        self.layout().addWidget(self.settings)
        self.layout().addWidget(self.map)
        self.layout().addWidget(self.evolution)

    def timerUpdate(self):
        while self.execution_queue:
            fun, args = self.execution_queue.pop(0)
            if not fun(*args):
                break

    def showEvolution(self, _=None):
        self.map.extends_button.set_text("")
        self.evolution.show()
        self._window.adjustSize()

    def hideEvolution(self, _=None):
        self.map.extends_button.set_text("➔")
        self.evolution.hide()
        self._window.centralWidget().adjustSize()
        self._window.adjustSize()

    def importCities(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            try:
                with open(file_dialog.selectedFiles()[0], "r") as file:
                    cities = json.loads(file.read())
                    assert isinstance(cities, list) and all(
                        isinstance(city, dict) and
                        "id" in city and "x" in city and "y" in city and
                        isinstance(city["x"], (int, float)) and
                        isinstance(city["y"], (int, float))
                        for city in cities
                    )
                    x_coords = [city["x"] for city in cities]
                    y_coords = [city["y"] for city in cities]
                    self.map.setCities(x_coords, y_coords)
                    self.settings.use_pregens_cities_input.setChecked(True)
            except Exception as e:
                print("Invalid file", e)

    def exportCities(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Cities File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                cities_data = [
                    {"id": idx, "x": x, "y": y}
                    for idx, (x, y) in enumerate(zip(self.map.cities_x, self.map.cities_y))
                ]
                with open(file_path, "w") as file:
                    json.dump(cities_data, file, indent=4)
            except Exception as e:
                print("Error saving file:", e)

    def runAlgorithm(self, num_cities, population_size, generations, mutation_rate, elitism, show_evolution, use_pregen_cities, use_stagnation_threshold):
        if use_pregen_cities and len(self.map.cities_x) == 0:
            return

        if self.tsp_genetic is not None:
            self.close_tsp = True
            self.tsp_thread.join()
            self.close_tsp = False

        self.execution_queue.clear()

        if show_evolution:
            self.evolution.clear()
            self.map.initTCP()
            self.showEvolution()
        else:
            self.settings.progress_bar.setRange(0, generations)
            self.settings.progress_bar.show()
            self.hideEvolution()

        self.show_evolution = show_evolution
        cities = numpy.array(tuple(zip(self.map.cities_x, self.map.cities_y))) if use_pregen_cities else None
        self.tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism, pre_gen_cities=cities, use_stagnation_threshold=use_stagnation_threshold, evolution_event=self.threadedReceiveGeneration, exit_event=self.threadedTSPEnded)
        # tsp_genetic = TSPPrim(num_cities)

        if not use_pregen_cities:
            self.map.setCities(*map(list, zip(*self.tsp_genetic.cities)))
        self.timer.start(PARAMS.evolution_animation_speed)

        self.tsp_thread = threading.Thread(target=self.tsp_genetic.run)
        self.tsp_thread.start()

    def threadedReceiveGeneration(self, gen_idx, population):
        if self.show_evolution:
            self.execution_queue.append( (self.evolution.updatePlot, (gen_idx, population, self.tsp_genetic.elit_count)) )
            self.execution_queue.append( (self.map.updatePlot, (gen_idx, *population[0])) )
        else:
            self.execution_queue.append( (lambda val: self.settings.progress_bar.setValue(val) or True, (gen_idx,)) )
        return self.close_tsp

    def threadedTSPEnded(self):
        self.execution_queue.insert( 0, (self.tspEnded, ()) )

    def tspEnded(self):
        if not self.show_evolution:
            self.map.updatePlot(0, self.tsp_genetic.best_path, self.tsp_genetic.best_distance)
            self.settings.progress_bar.hide()
            self.map.show()
            self._window.adjustSize()