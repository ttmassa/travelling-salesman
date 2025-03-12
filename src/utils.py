from PyQt5.QtWidgets import QPushButton

class Option:
    auto_start_animation: bool = True
    animation_speed: int = 200
    evolution_animation_speed: int = 100
    progressbar_refresh_time: int = 50

    default_num_cities: int = 10
    default_population_size: int = 100
    default_gen_count: int = 10
    default_mutation_rate: float = 0.03
    default_elitism: float = 0.1
    default_show_evolution: bool = True

PARAMS = Option()

def setButtonStyle(button, color):
    button.setStyleSheet(f"font-size: 14px; font-weight: bold; padding: 10px; border-radius: 5px; background-color: #{color};")

def makeButton(text, color, callback=None):
    button = QPushButton(text)
    setButtonStyle(button, color)
    if callback is not None:
        button.clicked.connect(callback)
    return button
