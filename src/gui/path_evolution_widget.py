from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PathEvolutionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.evolutions = []

    def initUI(self):
        layout = QVBoxLayout()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.previous_plot, = self.ax.plot([], [], 'r-')

        self.setLayout(layout)

    def update_plot(self):
        if self.evolutions:
            points_x, points_y = self.evolutions.pop(0)
            self.previous_plot.remove()
            self.previous_plot, = self.ax.plot(list(points_x) + [points_x[0]], list(points_y) + [points_y[0]], 'r-')
            self.canvas.draw()

