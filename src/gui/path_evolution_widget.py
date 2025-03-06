from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PathEvolutionWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout().addWidget(self.canvas)

        self.show_anim_button = QPushButton("Show Animation")
        self.layout().addWidget(self.show_anim_button)
        self.show_anim_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #394BED;")
        self.show_anim_button.clicked.connect(self.parent().showAnimation)
        self.show_anim_button.hide()

        self.previous_plot, = self.ax.plot([], [], 'r-')

    def updatePlot(self, points_x, points_y):
        self.previous_plot.remove()
        self.previous_plot, = self.ax.plot(list(points_x) + [points_x[0]], list(points_y) + [points_y[0]], 'r-')
        self.canvas.draw()

    def tspEnded(self):
        self.show_anim_button.show()
