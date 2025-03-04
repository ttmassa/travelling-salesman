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

        self.elit_count = int(self.elitism * self.population_size)

    def calculate_distance_matrix(self):
        # Initialize distance matrix : distance_matrix[i, j] = norm(cities[i] - cities[j])
        diff = self.cities[:, np.newaxis] - self.cities[np.newaxis, :]
        return np.linalg.norm(diff, axis=-1)

    def generate_population(self):
        # Each individual is a permutation of the cities
        population = [np.random.permutation(self.num_cities) for _ in range(self.population_size)]
        distances = [self.compute_individual_distance(ind) for ind in population]
        return list(zip(population, distances))

    def compute_individual_distance(self, individual):
        shifted_indices = np.roll(individual, -1)
        return np.sum(self.distance_matrix[individual, shifted_indices])

    def create_child(self, parent1, parent2):
        start, end = sorted(random.sample(range(self.num_cities), 2))
        # # Initialize child
        child = np.full(self.num_cities, -1)
        child[start:end] = parent1[start:end]
        parent1_genes = set(parent1[start:end])

        # empty_positions = np.where(child == -1)[0]
        # child[empty_positions] = [city for city in parent2 if city not in parent1_genes]

        # Fill the remaining positions with the genes from parent2
        current_pos = end % self.num_cities
        for city in parent2:
            if city not in parent1_genes:
                child[current_pos] = city
                current_pos = (current_pos + 1) % self.num_cities

        self.mutate(child)
        return (child, self.compute_individual_distance(child))

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            # Swap two random cities
            i, j = random.sample(range(self.num_cities), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def evolve(self):
        # Perform selection
        individuals, weights = zip(*self.population)
        new_population = [self.create_child(*random.choices(individuals, map(lambda x: 1 / (2**x), weights), k=2)) for _ in range(self.population_size - self.elit_count)]
        self.population = self.population[:self.elit_count] + new_population

    def run(self):
        best_route = None
        best_distance = float('inf')
        for i in range(self.generations):
            self.population.sort(key = lambda x: x[1])
            self.evolve()
            current_best_route = self.population[0]
            if not best_route or current_best_route[1] < best_route[1]:
                best_route = current_best_route
            if self.on_gen_update:
                if self.on_gen_update(i, [w for (_, w) in self.population]):
                    return
        # print(self.cities)
        # for i, city in enumerate(self.cities):
        #     print(f"City {i}: {city}")
        print(f"Best route: {best_route[0]}")
        print(f"Best distance: {best_route[1]}")

        self.best_route, self.best_distance = best_route
        self.is_ended = True
