from PyQt5.QtWidgets import QDialog, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QTimer
import threading
from params import PARAMS

from gui.pop_evolution_widget import PopEvolutionWidget
from gui.path_evolution_widget import PathEvolutionWidget
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

        if self.show_evolution:
            self.pop_evolution_widget = PopEvolutionWidget(self)
            self.layout().addWidget(self.pop_evolution_widget)

            self.path_evolution_widget = PathEvolutionWidget(self)
            self.path_evolution_widget.ax.plot(points_x, points_y, 'yo')
            self.layout().addWidget(self.path_evolution_widget)
        else:
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setRange(0, self.tsp_genetic.generations)
            self.layout().addWidget(self.progress_bar)

        self.best_path_widget = BestPathWidget(self, points_x, points_y)
        self.best_path_widget.hide()
        self.layout().addWidget(self.best_path_widget)

    def threadedReceiveGeneration(self, gen_idx, gen_distances, best_path):
        if self.show_evolution:
            self.execution_queue.append( (self.pop_evolution_widget.updatePlot, (gen_idx, gen_distances)) )
            self.execution_queue.append( (self.path_evolution_widget.updatePlot, (*best_path, gen_distances[0])) )
        else:
            QTimer.singleShot(0, lambda val=gen_idx: self.progress_bar.setValue(val))
        return self.shouldClose

    def threadedTSPEnded(self):
        self.execution_queue.insert( 0, (self.tspEnded, ()) )

    def timerUpdate(self):
        if self.execution_queue:
            fun, args = self.execution_queue.pop(0)
            fun(*args)

    def closeEvolutionWidget(self):
        self.pop_evolution_widget.close()
        self.adjustSize()

    def showAnimation(self):
        self.path_evolution_widget.close()
        self.best_path_widget.show()

    def closeEvent(self, a0):
        self.shouldClose = True
        self.tsp_thread.join(1.0)
        return super().closeEvent(a0)

    def tspEnded(self):
        if self.show_evolution:
            self.pop_evolution_widget.tspEnded()
            self.path_evolution_widget.tspEnded()

        self.points_x = [self.tsp_genetic.cities[e][0] for e in self.tsp_genetic.best_path] + [self.tsp_genetic.cities[self.tsp_genetic.best_path[0]][0]]
        self.points_y = [self.tsp_genetic.cities[e][1] for e in self.tsp_genetic.best_path] + [self.tsp_genetic.cities[self.tsp_genetic.best_path[0]][1]]
        self.best_path_widget.points_x = self.points_x
        self.best_path_widget.points_y = self.points_y
        self.best_path_widget.best_distance = self.tsp_genetic.best_distance

        if not self.show_evolution:
            self.progress_bar.close()
            self.best_path_widget.show()
            self.adjustSize()
