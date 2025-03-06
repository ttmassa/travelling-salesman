import pytest
import numpy as np
import time
from src.tsp_genetic import TSPGenetic
from src.tsp_genetic_old import TSPGenetic

def run_tsp_test(num_cities, population_size, gens, mutation_rate, elitism, reps_count):
    pre_gen_cities = np.random.rand(num_cities, 2)
    tsp1_time, tsp1_score = 0, 0
    tsp2_time, tsp2_score = 0, 0

    for _ in range(reps_count):
        tsp1 = TSPGenetic(num_cities, population_size, gens, mutation_rate, elitism, pre_gen_cities=pre_gen_cities)
        tsp2 = TSPGenetic(num_cities, population_size, gens, mutation_rate, elitism, pre_gen_cities=pre_gen_cities)
        
        t1 = time.time()
        tsp1.run()
        tsp1_time += time.time() - t1
        tsp1_score += tsp1.best_distance

        t1 = time.time()
        tsp2.run()
        tsp2_time += time.time() - t1
        tsp2_score += tsp2.best_distance
    
    return {
        "tsp1_avg_time": tsp1_time / reps_count,
        "tsp1_avg_score": tsp1_score / reps_count,
        "tsp2_avg_time": tsp2_time / reps_count,
        "tsp2_avg_score": tsp2_score / reps_count,
    }

@pytest.mark.parametrize("num_cities, population_size, generations, mutation_rate, elitism, reps_count", [
    (100, 100, 50, 0.03, 0.1, 10)
])
def test_tsp(num_cities, population_size, generations, mutation_rate, elitism, reps_count):
    results = run_tsp_test(num_cities, population_size, generations, mutation_rate, elitism, reps_count)
    
    print(f"TSP_cur {generations} gens: avg_time={results['tsp1_avg_time']}; avg_score={results['tsp1_avg_score']}")
    print(f"TSP_nex {generations} gens: avg_time={results['tsp2_avg_time']}; avg_score={results['tsp2_avg_score']}")
    
    assert results['tsp1_avg_score'] > 0, "TSP1 average score should be positive"
    assert results['tsp2_avg_score'] > 0, "TSP2 average score should be positive"