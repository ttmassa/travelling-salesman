import numpy as np
import math

class TSPNN: # Nearest Neighbor
    def __init__(self, num_cities, pre_gen_cities = None):
        self.num_cities = num_cities
        self.cities = pre_gen_cities if pre_gen_cities is not None else np.random.rand(num_cities, 2)
        self.cities_deg = [0] * num_cities
        self.distances = []
        self.on_evolution = None
        self.on_exit = None
        self.is_ended = False

    def setEvolutionEvent(self, on_gen_update):
        self.on_evolution = on_gen_update

    def setExitEvent(self, on_exit_update):
        self.on_exit = on_exit_update

    def distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def getNearestCity(self, available_cities, ref_city):
        min_dist, min_idx = float("inf"), 0
        for i in available_cities:
            dist = self.distance(self.cities[ref_city], self.cities[i])
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        return min_dist, min_idx

    def run(self):
        self.best_path = [0]
        available_cities = list(range(1, self.num_cities))
        self.best_distance = 0

        a_dist, a_idx = self.getNearestCity(available_cities, 0)
        self.best_path.append(a_idx)
        available_cities.remove(self.best_path[-1])
        self.best_distance += a_dist

        while available_cities:
            a_dist, a_idx = self.getNearestCity(available_cities, self.best_path[-1])
            available_cities.remove(a_idx)
            self.best_path.append(a_idx)

            self.best_distance += a_dist

            if self.on_evolution:
                self.on_evolution(0, [self.best_distance], zip(*map(lambda city: self.cities[city], self.best_path)))

        if self.on_exit:
            self.on_exit()
