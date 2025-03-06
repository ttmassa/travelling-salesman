from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QDialog
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PopEvolutionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.evolutions = []

    def initUI(self):
        layout = QVBoxLayout()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.canvas.draw()

    def update_plot(self):
        if self.evolutions:
            gen_index, points_y = self.evolutions.pop(0)
            self.ax.plot([gen_index] * len(points_y), points_y, 'ro')
            self.canvas.draw()

