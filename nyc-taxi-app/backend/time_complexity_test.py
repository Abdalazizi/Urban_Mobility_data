import time
import random
from custom_algorithm import manual_sort

def run_time_complexity_test():
    """
    Measures the execution time of the manual_sort function with different input sizes.
    """
    input_sizes = [100, 1000, 10000, 50000]
    print("Running time complexity test for manual_sort...\n")

    for size in input_sizes:
        data = [{'fare_per_km': random.uniform(1, 100)} for _ in range(size)]
        
        start_time = time.time()
        manual_sort(data, key='fare_per_km', descending=True)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        print(f"Input size: {size:<10} | Execution time: {execution_time:.6f} seconds")

if __name__ == '__main__':
    run_time_complexity_test()
