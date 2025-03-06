from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QDialog
from PyQt5.QtCore import Qt
from tsp_genetic import TSPGenetic
from gui.result_window import ResultWindow
from gui.evolution_window import EvolutionWindow
from params import PARAMS
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Genetic Algorithm")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title label
        self.label = QLabel("Welcome to the TSP Genetic Algorithm GUI", self)
        self.label.setStyleSheet("font-size: 24px;")
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setSizePolicy(self.label.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)
        layout.addWidget(self.label)

        layout.addSpacing(50)

        # Parameters layout
        parameters_layout = QVBoxLayout()
        parameters_layout.setAlignment(Qt.AlignHCenter)

        # Parameters label
        self.label = QLabel("Parameters", self)
        self.label.setStyleSheet("font-size: 18px; text-decoration: underline;")
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setSizePolicy(self.label.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)
        parameters_layout.addWidget(self.label)

        parameters_layout.addSpacing(30)

        # Form layout for parameters
        form_layout = QFormLayout()

        # Number of cities
        self.num_cities_input = QLineEdit(self)
        self.num_cities_input.setPlaceholderText(f"Number of cities (default: {PARAMS.default_num_cities})")
        form_layout.addRow("Number of cities:", self.num_cities_input)

        # Population size
        self.population_size_input = QLineEdit(self)
        self.population_size_input.setPlaceholderText(f"Population size (default: {PARAMS.default_population_size})")
        form_layout.addRow("Population size:", self.population_size_input)

        # Number of generations
        self.generations_input = QLineEdit(self)
        self.generations_input.setPlaceholderText(f"Number of generations (default: {PARAMS.default_gen_count})")
        form_layout.addRow("Number of generations:", self.generations_input)

        # Mutation rate
        self.mutation_rate_input = QLineEdit(self)
        self.mutation_rate_input.setPlaceholderText(f"Mutation rate (default: {PARAMS.default_mutation_rate})")
        form_layout.addRow("Mutation rate:", self.mutation_rate_input)

        # Elitism
        self.elitism_input = QLineEdit(self)
        self.elitism_input.setPlaceholderText(f"Elitism (default: {PARAMS.default_elitism})")
        form_layout.addRow("Elitism:", self.elitism_input)

        parameters_layout.addLayout(form_layout)
        layout.addLayout(parameters_layout)

        # Run button
        self.run_button = QPushButton("Run TSP Algorithm", self)
        self.run_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #39ED4B;")
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_algorithm(self):
        # Get the parameters from the input fields
        num_cities = int(self.num_cities_input.text()) if self.num_cities_input.text() else PARAMS.default_num_cities
        population_size = int(self.population_size_input.text()) if self.population_size_input.text() else PARAMS.default_population_size
        generations = int(self.generations_input.text()) if self.generations_input.text() else PARAMS.default_gen_count
        mutation_rate = float(self.mutation_rate_input.text()) if self.mutation_rate_input.text() else PARAMS.default_mutation_rate
        elitism = float(self.elitism_input.text()) if self.elitism_input.text() else PARAMS.default_elitism

        tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism)

        ResultWindow(tsp_genetic).exec()

        # if PARAMS.show_evolution:
        #     EvolutionWindow(num_cities, population_size, generations, mutation_rate, elitism)
        # else:
        #     # Create an instance of the TSPGenetic class
        #     t1 = time.time()
        #     tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism)
        #     t2 = time.time()
        #     print(t2 - t1)
        #     tsp_genetic.run()
        #     t3 = time.time()
        #     print(t3 - t2)

        #     # Show the result in a new window
        #     result_window = ResultWindow(tsp_genetic.best_route, tsp_genetic.best_distance, tsp_genetic.cities)
        #     result_window.exec_()

