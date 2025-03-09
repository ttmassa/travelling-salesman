import numpy as np
import random

class TSPGenetic:
    def __init__(self, num_cities, population_size, generations, mutation_rate, elitism, pre_gen_cities = None):
        self.num_cities = num_cities
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.cities = pre_gen_cities if pre_gen_cities is not None else np.random.rand(num_cities, 2)
        self.distance_matrix = self.calculateDistanceMatrix()
        self.population = self.generatePopulation()
        self.elit_count = int(self.elitism * self.population_size)
        self.on_evolution = None
        self.on_exit = None
        self.is_ended = False

    def setEvolutionEvent(self, on_gen_update):
        self.on_evolution = on_gen_update

    def setExitEvent(self, on_exit_update):
        self.on_exit = on_exit_update

    def calculateDistanceMatrix(self):
        # Initialize distance matrix : distance_matrix[i, j] = norm(cities[i] - cities[j])
        diff = self.cities[:, np.newaxis] - self.cities[np.newaxis, :]
        return np.linalg.norm(diff, axis=-1)

    def generatePopulation(self):
        # Each individual is a permutation of the cities
        population = [np.random.permutation(self.num_cities) for _ in range(self.population_size)]
        distances = [self.computeIndividualDistance(ind) for ind in population]
        return list(zip(population, distances))

    def computeIndividualDistance(self, individual):
        shifted_indices = np.roll(individual, -1)
        return np.sum(self.distance_matrix[individual, shifted_indices])

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

    def evolve(self):
        # Perform selection
        self.population = self.population[:self.elit_count]

        # Use the weights to select the fit individuals with higher probability
        new_population = [self.createChild(*random.sample(self.population, 2)) for _ in range(self.population_size - self.elit_count)]

        # Combine the elite individuals with the new population
        self.population += new_population

    def run(self):
        best_individual = None
        for i in range(self.generations):
            # Sort the population based on fitness
            self.population.sort(key = lambda x: x[1])
            self.evolve()
            current_best_individual = self.population[0]
            if not best_individual or current_best_individual[1] < best_individual[1]:
                best_individual = current_best_individual
            if self.on_evolution:
                self.on_evolution(i, [ind[1] for ind in self.population], best_individual[0], best_individual[1])
        self.best_path, self.best_distance = best_individual
        # print("Best path:", self.best_path)
        # print("Best distance:", self.best_distance)
        self.is_ended = True
        if self.on_exit:
            self.on_exit()