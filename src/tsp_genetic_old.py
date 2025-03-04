import numpy as np
import random

class TSPGenetic:
    def __init__(self, num_cities, population_size, generations, mutation_rate, elitism, on_gen_update = None):
        self.num_cities = num_cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.cities = np.random.rand(num_cities, 2)
        self.distance_matrix = self.calculate_distance_matrix()
        self.population = self.generate_population()
        self.on_gen_update = on_gen_update
        self.is_ended = False

    def calculate_distance_matrix(self):
        # Initialize distance matrix : distance_matrix[i, j] = norm(cities[i] - cities[j])
        diff = self.cities[:, np.newaxis] - self.cities[np.newaxis, :]
        return np.linalg.norm(diff, axis=-1)

    def generate_population(self):
        # Each individual is a permutation of the cities
        return np.array([np.random.permutation(self.num_cities) for _ in range(self.population_size)])

    def compute_total_distance(self, individual):
        shifted_indices = np.roll(individual, -1)
        return np.sum(self.distance_matrix[individual, shifted_indices])
    def fitness(self, individual):
        # Add a small epsilon to avoid division by zero
        # epsilon = 1e-10
        return 1 / self.compute_total_distance(individual)

    def selection(self):
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)
        # Keep the top half of the population
        sorted_population = sorted_population[:int(self.population_size * self.elitism)]
        return sorted_population

    def create_child(self, parent1, parent2):
        start, end = sorted(random.sample(range(self.num_cities), 2))
        # Initialize child 
        child = [-1] * self.num_cities
        # Copy the subsequence from parent1
        child[start:end] = parent1[start:end]

        # Fill the remaining positions with the genes from parent2
        current_pos = end % self.num_cities
        for city in parent2:
            if city not in child:
                while child[current_pos] != -1:
                    current_pos = (current_pos + 1) % self.num_cities
                child[current_pos] = city

        return np.array(child)

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            # Swap two random cities
            i, j = random.sample(range(self.num_cities), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def evolve(self):
        new_population = []
        # Perform selection
        selected_population = self.selection()
        # Populate new generation with childs from selected parents
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child = self.create_child(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        self.population = new_population

    def run(self):
        best_route = None
        best_distance = float('inf')
        for i in range(self.generations):
            self.evolve()
            current_best_route = max(self.population, key=lambda x: self.fitness(x))
            current_distance = 1 / self.fitness(current_best_route)
            if current_distance < best_distance:
                best_route = current_best_route
                best_distance = current_distance
            if self.on_gen_update:
                if self.on_gen_update(i, [1 / self.fitness(e) for e in self.population]):
                    return
        # print(self.cities)
        # for i, city in enumerate(self.cities):
        #     print(f"City {i}: {city}")
        print(f"Best route: {best_route}")
        print(f"Best distance: {best_distance}")

        self.best_route = best_route
        self.best_distance = best_distance
        self.is_ended = True
