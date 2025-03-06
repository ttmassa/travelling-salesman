from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import threading
from params import PARAMS

from gui.pop_evolution_widget import PopEvolutionWidget
from gui.path_evolution_widget import PathEvolutionWidget
from gui.best_path_widget import BestPathWidget

class ResultWindow(QDialog):
    def __init__(self, tsp_genetic):
        super().__init__()
        self.setWindowTitle("TSP Genetic Algorithm - Generation")
        # self.setFixedSize(1080, 720)
        self.tsp_genetic = tsp_genetic
        self.tsp_genetic.setEvolutionEvent(self.receiveGeneration)
        self.tsp_genetic.setExitEvent(self.tspEnded)
        self.shouldClose = False
        self.initUI()

        self.tsp_thread = threading.Thread(target=self.tsp_genetic.run)
        self.tsp_thread.start()

    def initUI(self):
        layout = QHBoxLayout()

        self.pop_evolution_widget = PopEvolutionWidget(self)
        layout.addWidget(self.pop_evolution_widget)

        self.path_evolution_widget = PathEvolutionWidget(self)
        self.path_evolution_widget.ax.plot(*zip(*self.tsp_genetic.cities), 'yo')
        layout.addWidget(self.path_evolution_widget)

        # self.best_path_widget = BestPathWidget(self)
        # layout.addWidget(self.best_path_widget)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateEvolution)
        self.timer.start(PARAMS.evolution_animation_speed)

    def receiveGeneration(self, gen_idx, gen_distances, best_path):
        self.pop_evolution_widget.evolutions.append( (gen_idx, gen_distances) )
        self.path_evolution_widget.evolutions.append( best_path)
        return self.shouldClose

    def updateEvolution(self):
        self.pop_evolution_widget.update_plot()
        self.path_evolution_widget.update_plot()

    def closeEvolutionWidget(self):
        self.pop_evolution_widget.close()

    def showAnimation(self):
        self.path_evolution_widget.close()
        # self.layout()

    def closeEvent(self, a0):
        self.shouldClose = True
        self.tsp_thread.join(1.0)
        return super().closeEvent(a0)

    def tspEnded(self):
        self.pop_evolution_widget.tspEnded()
        self.path_evolution_widget.tspEnded()