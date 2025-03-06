import sys
from gui.main_window import *

import tsp_genetic_old
import tsp_genetic
import numpy as np
import time

def main(argv):
    if "-tests" in argv:
      tests()
      sys.exit(0)
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def tests():
    num_cities, population_size, generations, mutation_rate, elitism = 200, 100, 5, 0.03, 0.1

    reps_count = 20
    pre_gen_cities = np.random.rand(num_cities, 2)
    for gens in range(100, 101):
        tsp1_time, tsp1_score = 0, 0
        tsp2_time, tsp2_score = 0, 0

        for _ in range(reps_count):
            tsp1 = tsp_genetic.TSPGenetic(num_cities, population_size, gens, mutation_rate, elitism, pre_gen_cities=pre_gen_cities)
            tsp2 = tsp_genetic_old.TSPGenetic(num_cities, population_size, gens, mutation_rate, elitism, pre_gen_cities=pre_gen_cities)
            t1 = time.time()
            tsp1.run()
            tsp1_time += time.time() - t1
            tsp1_score += tsp1.best_distance

            t1 = time.time()
            tsp2.run()
            tsp2_time += time.time() - t1
            tsp2_score += tsp2.best_distance

        print(f"TSP_cur {gens} gens: avg_time={tsp1_time / reps_count}; avg_score={tsp1_score / reps_count}")
        print(f"TSP_nex {gens} gens: avg_time={tsp2_time / reps_count}; avg_score={tsp2_score / reps_count}")




if __name__ == "__main__":
    main(sys.argv)