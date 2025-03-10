from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MapWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.paths = []

        # === INIT UI ===
        self.setLayout(QVBoxLayout())

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        self.ax.set_title("Current Best Distance")
        self.edges = self.ax.plot([], [], 'go', label="Start City") + self.ax.plot([], [], 'ro', label="City")
        self.vertices = self.ax.plot([], [], 'b-', label="Path")
        self.ax.legend()
        self.layout().addWidget(self.canvas)

        # Absolute position button
        # self.run_button = QPushButton("X", self)
        # self.run_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 0px; border-radius: 5px; background-color: #ED394B;")

        buttons_layout = QHBoxLayout()

        self.previous_button = QPushButton("Previous")
        self.previous_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        buttons_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("next")
        self.next_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        buttons_layout.addWidget(self.next_button)

        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        buttons_layout.addWidget(self.play_button)


        self.layout().addLayout(buttons_layout)

        self.hide()

    def remove(self, obj, count):
        for i in range(count):
            obj.pop().remove()

    def setCities(self, points_x, points_y):
        self.remove(self.edges, len(self.edges))
        self.edges = self.ax.plot(points_x, points_y, 'ro', label="City")
        self.canvas.draw()
        self.cities_x, self.cities_y = points_x, points_y

    def moveCity(self, city, x, y):
        self.cities_x[city], self.cities_y[city] = x, y
        self.setCities(self.cities_x, self.cities_y)

    def setPath(self, path):
        self.remove(self.vertices, len(self.vertices))
        points_x = [self.cities_x[city] for city in path]
        points_y = [self.cities_y[city] for city in path]
        self.vertices = self.ax.plot(list(points_x) + [points_x[0]], list(points_y) + [points_y[0]], 'b-')
        self.canvas.draw()

    def updatePlot(self, generation, path, distance):
        self.setPath(path)
        self.ax.set_title(f"Current Best Distance : {distance:.5f}")
