import numpy as np
import random

class TSPGenetic:
    def __init__(self, num_cities=10, population_size=100, generations=500, mutation_rate=0.01):
        self.num_cities = num_cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.cities = np.random.rand(num_cities, 2)
        self.distance_matrix = self.calculate_distance_matrix()
        self.population = self.generate_population()

    def calculate_distance_matrix(self):
        # Initialize distance matrix
        distance_matrix = np.zeros((self.num_cities, self.num_cities))
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    distance_matrix[i, j] = np.linalg.norm(self.cities[i] - self.cities[j])
        return distance_matrix

    def generate_population(self):
        population = []
        for _ in range(self.population_size):
            # Each individual is a permutation of the cities
            individual = np.random.permutation(self.num_cities)
            population.append(individual)
        return population

    def fitness(self, individual, distance_matrix):
        total_distance = 0
        for i in range(len(individual)):
            from_city = individual[i]
            to_city = individual[(i + 1) % len(individual)]
            total_distance += distance_matrix[from_city, to_city]
        return 1 / total_distance
    
    def selection(self):
        sorted_population = sorted(self.population, key=lambda x: self.fitness(x, self.distance_matrix), reverse=True)
        # Keep the top half of the population
        sorted_population = sorted_population[:self.population_size // 2]
        return sorted_population