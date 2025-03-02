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

    def fitness(self, individual):
        total_distance = 0
        for i in range(len(individual)):
            from_city = individual[i]
            to_city = individual[(i + 1) % len(individual)]
            total_distance += self.distance_matrix[from_city, to_city] 
        # Add a small epsilon to avoid division by zero
        epsilon = 1e-10
        return 1 / (total_distance + epsilon)
    
    def selection(self):
        sorted_population = sorted(self.population, key=self.fitness, reverse=True)
        # Keep the top half of the population
        sorted_population = sorted_population[:self.population_size // 2]
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
        for _ in range(self.generations):
            self.evolve()
            current_best_route = max(self.population, key=lambda x: self.fitness(x))
            current_distance = 1 / self.fitness(current_best_route)
            if current_distance < best_distance:
                best_route = current_best_route
                best_distance = current_distance
        print(self.cities)
        for i, city in enumerate(self.cities):
            print(f"City {i}: {city}")
        print(f"Best route: {best_route}")
        print(f"Best distance: {best_distance}")
        return best_route, best_distance
