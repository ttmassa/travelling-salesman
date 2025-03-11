from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class MapWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.paths = []
        self.path_index = 0
        self.cities_x, self.cities_y = [], []

        # === INIT UI ===
        self.setLayout(QVBoxLayout())

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_xlabel("longitude")
        self.ax.set_ylabel("latitude")
        self.ax.set_title("Path")
        self.edges = self.ax.plot([], [], 'go', label="Start City") + self.ax.plot([], [], 'ro', label="City")
        self.vertices = self.ax.plot([], [], 'b-', label="Path")
        self.ax.legend()
        self.layout().addWidget(self.canvas)

        self.buttons = QWidget()
        buttons_layout = QHBoxLayout()

        previous_button = QPushButton("Previous")
        previous_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        previous_button.clicked.connect(self.previousPath)
        buttons_layout.addWidget(previous_button)

        next_button = QPushButton("next")
        next_button.clicked.connect(self.nextPath)
        next_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        buttons_layout.addWidget(next_button)

        play_button = QPushButton("Play")
        play_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #5060FF;")
        buttons_layout.addWidget(play_button)

        buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons.setLayout(buttons_layout)
        self.buttons.hide()
        self.layout().addWidget(self.buttons)

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

    def previousPath(self):
        if self.path_index <= 0:
            return
        self.path_index -= 1
        self.setPath(self.paths[self.path_index])

    def nextPath(self):
        if self.path_index >= len(self.paths) - 1:
            return
        self.path_index += 1
        self.setPath(self.paths[self.path_index])

    def updatePlot(self, generation, path, distance):
        self.ax.set_title(f"Path Distance : {distance:.5f}")
        self.setPath(path)
        self.paths.append(path)

        self.buttons.show()

