from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PopEvolutionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.evolutions = []

    def initUI(self):
        self.setLayout(QVBoxLayout())

        # Title
        self.title = QLabel("Population Evolution", self)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignHCenter)
        self.layout().addWidget(self.title)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout().addWidget(self.canvas)

        self.close_button = QPushButton("Close Evolution Widget", self)
        self.close_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #A0A0A0;")
        self.close_button.clicked.connect(self.parent().closeEvolutionWidget)
        self.close_button.hide()
        self.layout().addWidget(self.close_button)

    def updatePlot(self, gen_index, points_y):
        self.ax.plot([gen_index] * len(points_y), points_y, 'ro')
        self.canvas.draw()

    def tspEnded(self):
        self.close_button.show()