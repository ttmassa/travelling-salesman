from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class EvolutionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.points = []

    def initUI(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlabel("generation")
        self.ax.set_ylabel("distance")
        self.ax.set_title("Population Evolution")
        self.ax.legend(handles=self.ax.plot([], [], 'ro', label="Individual") + self.ax.plot([], [], 'go', label="Elit"))

        main_layout.addWidget(self.canvas)

        self.close_button = self.ax.text(1.1, 1.1, 'x', transform=self.ax.transAxes,
                                      fontsize=12, fontweight='400', color='black',
                                      ha='right', va='bottom', bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))
        self.close_button.set_picker(True)
        self.canvas.mpl_connect('pick_event', self.parent().hideEvolution)

        self.hide()

    def clear(self):
        while self.points:
            self.points.pop().remove()

    def updatePlot(self, gen_index, population, elit_count):
        _, points_y = zip(*population)
        self.points += self.ax.plot([gen_index] * (len(points_y) - elit_count), points_y[elit_count:], 'ro') + \
                       self.ax.plot([gen_index] * elit_count, points_y[:elit_count], 'go')
        self.canvas.draw()
