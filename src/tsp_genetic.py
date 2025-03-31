import numpy as np
import random
import math
from utils import PARAMS

class TSPGenetic:
    def __init__(self, num_cities, population_size, generations, mutation_rate, elitism, pre_gen_cities=None, use_stagnation_threshold=False, evolution_event=None, exit_event=None):
        self.num_cities = len(pre_gen_cities) if pre_gen_cities is not None else num_cities
        assert 4 <= self.num_cities and 10 <= population_size and 1 <= generations and 0 <= mutation_rate <= 1 and 2 <= population_size * elitism < population_size, "Domain Error"

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.cities = pre_gen_cities if pre_gen_cities is not None else np.random.rand(num_cities, 2) * [PARAMS.default_cities_x, PARAMS.default_cities_y]
        self.distance_matrix = self.calculateDistanceMatrix()
        self.population = self.generatePopulation()
        self.elit_count = int(elitism * self.population_size)
        self.stagnation_threshold = self.computeStagnationThreshold() if use_stagnation_threshold else float('inf')
        self.on_evolution = evolution_event
        self.on_exit = exit_event
        self.is_ended = False


    def calculateDistanceMatrix(self):
        # Initialize distance matrix : distance_matrix[i, j] = norm(cities[i] - cities[j])
        diff = self.cities[:, np.newaxis] - self.cities[np.newaxis, :]
        return np.linalg.norm(diff, axis=-1)

    def generatePopulation(self):
        # Each individual is a permutation of the cities
        population = [np.random.permutation(self.num_cities) for _ in range(self.population_size)]
        distances = [self.computeIndividualDistance(ind) for ind in population]
        return sorted(zip(population, distances), key = lambda x: x[1])

    def computeIndividualDistance(self, individual):
        shifted_indices = np.roll(individual, -1)
        return np.sum(self.distance_matrix[individual, shifted_indices])
    
    def computeStagnationThreshold(self):
        return PARAMS.default_stagnation_alpha * math.log(self.num_cities * self.population_size) / (self.mutation_rate * self.elit_count)
        
    def createChild(self, parent1, parent2):
        parent1, parent2 = parent1[0], parent2[0]
        start, end = sorted(random.sample(range(self.num_cities), 2))
        # Initialize child
        child = np.full(self.num_cities, -1)
        child[start:end] = parent1[start:end]
        parent1_genes = set(parent1[start:end])

        # Fill the remaining positions with the genes from parent2
        current_pos = end % self.num_cities
        for city in parent2:
            if city not in parent1_genes:
                child[current_pos] = city
                current_pos = (current_pos + 1) % self.num_cities

        self.mutate(child)
        return (child, self.computeIndividualDistance(child))

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            # Swap two random cities
            i, j = random.sample(range(self.num_cities), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def selection(self):
        # Perform selection
        self.population = self.population[:self.elit_count]

    def evolve(self):
        # Use the weights to select the fit individuals with higher probability
        new_population = [self.createChild(*random.sample(self.population, 2)) for _ in range(self.population_size - self.elit_count)]

        # Combine the elite individuals with the new population
        self.population += new_population

    def run(self):
        best_individual = None
        stagnation_counter = 0
        for i in range(self.generations):
            self.selection()
            self.evolve()
            # Sort the population based on fitness
            self.population.sort(key = lambda x: x[1])
            current_best_individual = self.population[0]
            if not best_individual or current_best_individual[1] < best_individual[1]:
                best_individual = current_best_individual
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            if stagnation_counter >= self.stagnation_threshold:
                break
            if self.on_evolution:
                if self.on_evolution(i, self.population):
                    return

        self.best_path, self.best_distance = best_individual
        self.is_ended = True
        if self.on_exit:
            self.on_exit()
