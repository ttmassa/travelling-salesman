import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from tsp_genetic import TSPGenetic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Genetic Algorithm")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to the TSP Genetic Algorithm GUI", self)
        self.label.setStyleSheet("font-size: 24px;")
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label)

        self.run_button = QPushButton("Run TSP Algorithm", self)
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_algorithm(self):
        # Create an instance of the TSPGenetic class
        tsp_genetic = TSPGenetic(num_cities=10 ,population_size=100, generations=500, mutation_rate=0.01)
        tsp_genetic.run()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())