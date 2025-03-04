from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from gui.result_window import ResultWindow
from tsp_genetic import TSPGenetic
from params import PARAMS
import threading

class EvolutionWindow(QDialog):
    def __init__(self, num_cities, population_size, generations, mutation_rate, elitism):
        super().__init__()
        self.setWindowTitle("TSP Evolution Diagram")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        self.show()
        self.evolutions = []

        self.tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism, on_gen_update=self.update)
        threading.Thread(target=self.tsp_genetic.run).start()

    def initUI(self):
        layout = QVBoxLayout()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(PARAMS.evolution_animation_speed)

        self.setLayout(layout)
        self.canvas.draw()

    def update(self, gen_index, points_y):
        self.evolutions.append((gen_index, points_y))
        return not self.isVisible()

    def update_plot(self):
        if self.evolutions:
            gen_index, points_y = self.evolutions.pop(0)
            self.ax.plot([gen_index] * len(points_y), points_y, 'ro')
            self.canvas.draw()

    def closeEvent(self, a0):
        R = super().closeEvent(a0)
        if self.tsp_genetic.is_ended:
            result_window = ResultWindow(self.tsp_genetic.best_route, self.tsp_genetic.best_distance, self.tsp_genetic.cities)
            result_window.exec_()
        return R
