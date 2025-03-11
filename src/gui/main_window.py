from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer
import threading
from tsp_genetic import TSPGenetic
from gui.settings_widget import SettingsWidget
from gui.map_widget import MapWidget
from gui.evolution_widget import EvolutionWidget
from params import PARAMS
import numpy

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._window = QMainWindow()
        self._window.setWindowTitle("TSP Genetic Algorithm")
        self._window.move(100, 100)

        self.setLayout(QHBoxLayout())


        self.settings = SettingsWidget(self)
        self.map = MapWidget(self)
        self.evolution = EvolutionWidget(self)
        self.layout().addWidget(self.evolution)
        self.layout().addWidget(self.settings)
        self.layout().addWidget(self.map)

        self._window.setCentralWidget(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)
        self.execution_queue = []
        self.tsp_genetic = None
        self.show_evolution = False
        self.close_tsp = False

        self._window.show()

    def timerUpdate(self):
        while self.execution_queue:
            fun, args = self.execution_queue.pop(0)
            if not fun(*args):
                break

    def runAlgorithm(self, num_cities, population_size, generations, mutation_rate, elitism, show_evolution, use_pregen_cities):
        if use_pregen_cities and len(self.map.cities_x) == 0:
            return

        if self.tsp_genetic is not None:
            self.close_tsp = True
            self.tsp_thread.join()
            self.close_tsp = False

        self.execution_queue.clear()

        # self.settings.hide()
        if show_evolution:
            self.evolution.clear()
            self.evolution.show()
            self.map.show()
        else:
            self.evolution.hide()
            self.settings.progress_bar.setRange(0, generations)
            self.settings.progress_bar.show()
        self._window.adjustSize()

        self.show_evolution = show_evolution
        cities = numpy.array(tuple(zip(self.map.cities_x, self.map.cities_y))) if use_pregen_cities else None
        self.tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism, pre_gen_cities=cities, evolution_event=self.threadedReceiveGeneration, exit_event=self.threadedTSPEnded)
        # tsp_genetic = TSPPrim(num_cities)

        self.map.paths = []
        if not use_pregen_cities:
            self.map.setCities(*zip(*self.tsp_genetic.cities))
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