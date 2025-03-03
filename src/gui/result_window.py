from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResultWindow(QDialog):
    def __init__(self, best_path, best_distance, cities, parent=None):
        super().__init__(parent)
        self.best_path = best_path
        self.best_distance = best_distance
        self.cities = cities
        self.setWindowTitle("TSP Result")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Result label
        result_label = QLabel(f"Best Distance: {self.best_distance}", self)
        result_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        result_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(result_label)

        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.setAlignment(Qt.AlignLeft)

        # Start legend
        start_legend_layout = QHBoxLayout()
        start_legend = QLabel("Start city: ", self)
        start_legend.setStyleSheet("font-size: 14px; font-weight: bold;")
        start_legend_layout.addWidget(start_legend, alignment=Qt.AlignCenter)
        legend_layout.addLayout(start_legend_layout)

        start_color = QLabel(self)
        start_color.setFixedSize(10, 10)
        start_color.setStyleSheet("background-color: green; border-radius: 5px;")
        start_legend_layout.addWidget(start_color, alignment=Qt.AlignCenter)

        legend_layout.addSpacing(20)

        layout.addLayout(legend_layout)

        self.setLayout(layout)

        # Plot the best path
        self.plot_best_path()

    def plot_best_path(self):
        fig, ax = plt.subplots()
        x = [self.cities[i][0] for i in self.best_path]
        y = [self.cities[i][1] for i in self.best_path]

        # Close the cycle by adding the start city at the end
        x.append(x[0])
        y.append(y[0])

        # Plot the path
        ax.plot(x, y, marker='o', linestyle='-', color='b')

        # Highlight the start city
        ax.plot(x[0], y[0], marker='o', linestyle='-', color='g', label='Start')

        # Annotate each city
        for i, city_index in enumerate(self.best_path):
            ax.annotate(str(city_index), (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

        ax.set_title("Best Path")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")

        canvas = FigureCanvas(fig)
        self.layout().addWidget(canvas)