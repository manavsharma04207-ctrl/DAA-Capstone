import time
import random
from prioritization import knapsack_01_optimizer

def benchmark():
    input_sizes = [10, 50, 100, 200, 300]
    knapsack_times = []
    
    for size in input_sizes:
        parcels = [{'id': f'P{i}', 'weight_kg': random.randint(1, 15), 'priority_score': random.randint(10, 100)} for i in range(size)]
        t0 = time.time()
        knapsack_01_optimizer(parcels, max_capacity=100)
        knapsack_times.append((time.time() - t0) * 1000) # In milliseconds
        
    print("--- Benchmark Results ---")
    for size, t in zip(input_sizes, knapsack_times):
        print(f"Dataset Size N={size}: {t:.3f} ms")

if __name__ == '__main__':
    benchmark()