import threading
from PyQt5.QtWidgets import QDialog, QHBoxLayout
from PyQt5.QtCore import QTimer
from params import PARAMS
from gui.pop_evolution_widget import PopEvolutionWidget
from gui.best_path_widget import BestPathWidget

class ResultWindow(QDialog):
    def __init__(self, tsp_genetic, show_evolution):
        super().__init__()
        self.setWindowTitle("TSP Genetic Algorithm - Generation")
        self.move(100, 100)
        self.tsp_genetic = tsp_genetic
        self.show_evolution = show_evolution
        self.tsp_genetic.setEvolutionEvent(self.threadedReceiveGeneration)
        self.tsp_genetic.setExitEvent(self.threadedTSPEnded)
        self.shouldClose = False
        self.execution_queue = []
        self.initUI()

        self.tsp_thread = threading.Thread(target=self.tsp_genetic.run)
        self.tsp_thread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)
        self.timer.start(PARAMS.evolution_animation_speed)

    def initUI(self):
        self.setLayout(QHBoxLayout())

        points_x, points_y = zip(*self.tsp_genetic.cities)
        self.best_path_widget = BestPathWidget(self, points_x, points_y)
        self.layout().addWidget(self.best_path_widget)

        if self.show_evolution:
            self.pop_evolution_widget = PopEvolutionWidget(self)
            self.layout().addWidget(self.pop_evolution_widget)

    def threadedReceiveGeneration(self, gen_idx, gen_distances, best_path, best_distance):
        self.execution_queue.append((
            self.best_path_widget.addBestPath, 
            (best_path, best_distance, self.tsp_genetic.cities.copy())
        ))
        if self.show_evolution:
            self.execution_queue.append((self.pop_evolution_widget.updatePlot, (gen_idx, gen_distances)))
        return self.shouldClose

    def threadedTSPEnded(self):
        self.execution_queue.insert(0, (self.tspEnded, ()))
        self.execution_queue.insert(0, (self.best_path_widget.tspEnded, ()))

    def timerUpdate(self):
        if self.execution_queue:
            fun, args = self.execution_queue.pop(0)
            fun(*args)

    def closeEvolutionWidget(self):
        self.pop_evolution_widget.close()
        self.adjustSize()

    def showAnimation(self):
        self.best_path_widget.show()

    def closeEvent(self, a0):
        self.shouldClose = True
        self.tsp_thread.join(1.0)
        return super().closeEvent(a0)

    def tspEnded(self):
        if self.show_evolution:
            self.pop_evolution_widget.tspEnded()

        self.best_path_widget.addBestPath(
            self.tsp_genetic.best_path,
            self.tsp_genetic.best_distance,
            self.tsp_genetic.cities.copy()
        )
        self.adjustSize()