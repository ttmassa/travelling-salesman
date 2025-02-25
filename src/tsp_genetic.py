import numpy as np
import random

class TSPGenetic:
    def __init__(self, num_cities=10, population_size=100, generations=500, mutation_rate=0.01):
        self.num_cities = num_cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.cities = np.random.rand(num_cities, 2)
        self.population = self.generate_population()

    def generate_population(self):
        return [random.sample(range(self.num_cities), self.num_cities) for _ in range(self.population_size)]
    