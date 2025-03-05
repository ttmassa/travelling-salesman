
class Option:
    show_evolution: bool = True

    animated: bool = True
    auto_start: bool = True
    animation_speed: int = 200
    evolution_animation_speed: int = 100

    default_num_cities: int = 10
    default_population_size: int = 100
    default_gen_count: int = 50
    default_mutation_rate: float = 0.01
    default_elitism: float = 0.1

PARAMS = Option()
