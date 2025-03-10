from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class EvolutionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.points = []

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlabel("generation")
        self.ax.set_ylabel("distance")
        self.ax.set_title("Population Evolution")
        self.ax.legend(handles=self.ax.plot([], [], 'ro', label="Individual") + self.ax.plot([], [], 'go', label="Elit"))
        self.layout().addWidget(self.canvas)

        # self.close_button = QPushButton("Close Evolution Widget", self)
        # self.close_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #ED394B;")
        # self.close_button.clicked.connect(self.parent().closeEvolutionWidget)
        # self.close_button.hide()
        # self.layout().addWidget(self.close_button)

        self.hide()

    def clear(self):
        while self.points:
            self.points.pop().remove()

    def updatePlot(self, gen_index, population, elit_count):
        _, points_y = zip(*population)
        self.points += self.ax.plot([gen_index] * (len(points_y) - elit_count), points_y[elit_count:], 'ro') + \
                       self.ax.plot([gen_index] * elit_count, points_y[:elit_count], 'go')
        self.canvas.draw()
