from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
from tsp_genetic import TSPGenetic
from gui.result_window import ResultWindow
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from params import PARAMS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Genetic Algorithm")
        self.move(100, 100)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

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
        self.num_cities_input.setPlaceholderText(f"default: {PARAMS.default_num_cities}")
        self.num_cities_input.setValidator(QIntValidator(1, 999999, self))
        form_layout.addRow("Number of cities:", self.num_cities_input)

        # Population size
        self.population_size_input = QLineEdit(self)
        self.population_size_input.setPlaceholderText(f"default: {PARAMS.default_population_size}")
        self.population_size_input.setValidator(QIntValidator(1, 999999, self))
        form_layout.addRow("Population size:", self.population_size_input)

        # Number of generations
        self.generations_input = QLineEdit(self)
        self.generations_input.setPlaceholderText(f"default: {PARAMS.default_gen_count}")
        self.generations_input.setValidator(QIntValidator(1, 999999, self))
        form_layout.addRow("Number of generations:", self.generations_input)

        # Mutation rate
        self.mutation_rate_input = QLineEdit(self)
        self.mutation_rate_input.setPlaceholderText(f"default: {PARAMS.default_mutation_rate}")
        self.mutation_rate_input.setValidator(QDoubleValidator(0, 1, 10, self))
        form_layout.addRow("Mutation rate:", self.mutation_rate_input)

        # Elitism
        self.elitism_input = QLineEdit(self)
        self.elitism_input.setPlaceholderText(f"default: {PARAMS.default_elitism}")
        self.elitism_input.setValidator(QDoubleValidator(0, 1, 10, self))
        form_layout.addRow("Elitism:", self.elitism_input)

        # Show Evolution
        self.show_evolution_input = QCheckBox(self)
        self.show_evolution_input.setChecked(PARAMS.default_show_evolution)
        form_layout.addRow("Show evolution:", self.show_evolution_input)

        parameters_layout.addLayout(form_layout)
        layout.addLayout(parameters_layout)

        layout.addSpacing(50)

        # Run button
        self.run_button = QPushButton("Run TSP Algorithm", self)
        self.run_button.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #39ED4B;")
        self.run_button.clicked.connect(self.runAlgorithm)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def runAlgorithm(self):
        # Get the parameters from the input fields
        num_cities = int(self.num_cities_input.text()) if self.num_cities_input.text() else PARAMS.default_num_cities
        population_size = int(self.population_size_input.text()) if self.population_size_input.text() else PARAMS.default_population_size
        generations = int(self.generations_input.text()) if self.generations_input.text() else PARAMS.default_gen_count
        mutation_rate = float(self.mutation_rate_input.text()) if self.mutation_rate_input.text() else PARAMS.default_mutation_rate
        elitism = float(self.elitism_input.text()) if self.elitism_input.text() else PARAMS.default_elitism

        tsp_genetic = TSPGenetic(num_cities, population_size, generations, mutation_rate, elitism)

        self.hide()
        ResultWindow(tsp_genetic, self.show_evolution_input.isChecked()).exec()
        self.show()
