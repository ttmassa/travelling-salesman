from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout, QLineEdit, QSizePolicy, QCheckBox, QProgressBar
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from utils import PARAMS, makeButton

class SettingsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignHCenter)

        # Parameters label
        self.label = QLabel("Parameters", self)
        self.label.setStyleSheet("font-size: 18px; text-decoration: underline;")
        self.label.setAlignment(Qt.AlignHCenter)
        self.label.setSizePolicy(self.label.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)
        self.layout().addWidget(self.label)

        self.layout().addSpacing(30)

        # Form layout for parameters
        form_layout = QFormLayout()

        # Number of cities
        self.num_cities_input = QLineEdit(self)
        self.num_cities_input.setMinimumWidth(100)
        self.num_cities_input.setPlaceholderText(f"default: {PARAMS.default_num_cities}")
        self.num_cities_input.setValidator(QIntValidator(1, 999999, self))
        self.num_cities_input.textChanged.connect(lambda _: self.num_cities_input.setStyleSheet("color: #000;"))
        form_layout.addRow("Number of cities:", self.num_cities_input)

        # Population size
        self.population_size_input = QLineEdit(self)
        self.population_size_input.setPlaceholderText(f"default: {PARAMS.default_population_size}")
        self.population_size_input.setValidator(QIntValidator(1, 999999, self))
        self.population_size_input.textChanged.connect(lambda _: self.population_size_input.setStyleSheet("color: #000;"))
        form_layout.addRow("Population size:", self.population_size_input)

        # Number of generations
        self.generations_input = QLineEdit(self)
        self.generations_input.setPlaceholderText(f"default: {PARAMS.default_gen_count}")
        self.generations_input.setValidator(QIntValidator(1, 999999, self))
        self.generations_input.textChanged.connect(lambda _: self.generations_input.setStyleSheet("color: #000;"))
        form_layout.addRow("Number of generations:", self.generations_input)

        # Mutation rate
        self.mutation_rate_input = QLineEdit(self)
        self.mutation_rate_input.setPlaceholderText(f"default: {PARAMS.default_mutation_rate}")
        self.mutation_rate_input.setValidator(QDoubleValidator(0, 1, 10, self))
        self.mutation_rate_input.textChanged.connect(lambda _: self.mutation_rate_input.setStyleSheet("color: #000;"))
        form_layout.addRow("Mutation rate:", self.mutation_rate_input)

        # Elitism
        self.elitism_input = QLineEdit(self)
        self.elitism_input.setPlaceholderText(f"default: {PARAMS.default_elitism}")
        self.elitism_input.setValidator(QDoubleValidator(0, 1, 10, self))
        self.elitism_input.textChanged.connect(lambda _: self.elitism_input.setStyleSheet("color: #000;"))
        form_layout.addRow("Elitism:", self.elitism_input)

        self.layout().addLayout(form_layout)

        # Show Evolution
        self.show_evolution_input = QCheckBox("Show evolution", self)
        self.show_evolution_input.setChecked(PARAMS.default_show_evolution)
        self.layout().addWidget(self.show_evolution_input)

        # Stagnation threshold
        self.stagnation_threshold_input = QCheckBox("Use stagnation threshold", self)
        self.stagnation_threshold_input.setChecked(PARAMS.default_stagnation_threshold)
        self.layout().addWidget(self.stagnation_threshold_input)

        # Use Pre-Generated Cities
        self.use_pregens_cities_input = QCheckBox("Use pre-generated cities", self)
        # self.use_pregens_cities_input.clicked.connect(lambda _: self.parent().map.show() or self.parent()._window.adjustSize())
        self.layout().addWidget(self.use_pregens_cities_input)

        # Import cities button
        self.import_button = makeButton("Import cities", "CDCDDD")
        self.layout().addWidget(self.import_button)

        self.export_button = QPushButton("Export data", self)
        self.export_button.hide()
        self.layout().addWidget(self.export_button)

        self.layout().addSpacing(50)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        self.layout().addWidget(self.progress_bar)

        # Run button
        self.run_button = makeButton("Run TSP Algorithm", "39ED4B", self.runAlgorithm)
        self.layout().addWidget(self.run_button)

    def runAlgorithm(self):
        # Get the parameters from the input fields
        num_cities = int(self.num_cities_input.text() or PARAMS.default_num_cities)
        population_size = int(self.population_size_input.text() or PARAMS.default_population_size)
        generations = int(self.generations_input.text() or PARAMS.default_gen_count)
        mutation_rate = float(self.mutation_rate_input.text() or PARAMS.default_mutation_rate)
        elitism = float(self.elitism_input.text() or PARAMS.default_elitism)
        show_evolution = self.show_evolution_input.isChecked()
        use_stagnation_threshold = self.stagnation_threshold_input.isChecked()
        use_pregen_cities = self.use_pregens_cities_input.isChecked()

        if num_cities < 4:
            self.num_cities_input.setStyleSheet("color: #F00;")
        elif population_size < 10:
            self.population_size_input.setStyleSheet("color: #F00;")
        elif generations < 1:
            self.generations_input.setStyleSheet("color: #F00;")
        elif mutation_rate < 0 or mutation_rate > 1:
            self.mutation_rate_input.setStyleSheet("color: #F00;")
        elif elitism >= 1 or population_size * elitism < 2:
            self.elitism_input.setStyleSheet("color: #F00;")
        else:
            self.parent().runAlgorithm(num_cities, population_size, generations, mutation_rate, elitism, show_evolution, use_pregen_cities, use_stagnation_threshold)
