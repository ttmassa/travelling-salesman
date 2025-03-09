import pytest
import numpy as np
import time
from src.tsp_algo import TSPKruskal, TSPPrim

def test_tsp_kruskal_speed():
    num_cities = 100
    cities = np.random.rand(num_cities, 2)
    tsp = TSPKruskal(num_cities, cities)

    start_time = time.time()
    tsp.run()
    end_time = time.time()

    elapsed_time = end_time - start_time
    assert elapsed_time < 1

def test_tsp_prim_speed():
    num_cities = 100
    cities = np.random.rand(num_cities, 2)
    tsp = TSPPrim(num_cities, cities)

    start_time = time.time()
    tsp.run()
    end_time = time.time()

    elapsed_time = end_time - start_time
    assert elapsed_time < 1  

if __name__ == "__main__":
    pytest.main()