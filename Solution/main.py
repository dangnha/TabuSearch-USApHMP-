import time
from utils import tabu_search
from data import initial_parameter

# experements = ["10.2", "10.3", "10.4", "20.2", "20.3", "20.4", "40.2", "40.3", "40.4", "50.2", "50.3", "50.4", "100.2", "100.3", "100.4"]
experements = ["100.3", "100.4"]


for file_db in experements:
    n, p, alpha, delta, ksi, coords, weights, distances = initial_parameter(file_db)
    tabu_tenure = 5

    times = []
    cost = []
    dic = {}
    iter = 0
    
    if n <= 20:
        iter = 20
    elif n == 30:
        iter = 10
    elif n == 40:
        iter = 5
    elif n > 40:
        iter = 2
        
    # Run the Tabu Search
    for i in range(iter):
        start_time = time.time()
        best_hubs, best_assignments, best_cost, path = tabu_search(tabu_tenure, n, p, weights, distances, alpha, delta, ksi)
        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        cost.append(best_cost)
        dic[best_cost] = [best_hubs, best_assignments, path]

    best_cost = min(cost)
    best_hubs = dic[best_cost][0]
    best_assignments = dic[best_cost][1]
    tabu_list = dic[best_cost][2]
    timee = min(times)

    # Convert best_assignments to 1-based index for clearer output
    best_assignments_1_based = [x + 1 for x in best_assignments]
    best_hubs_1_based = [x + 1 for x in best_hubs]

    # Output the results
    print(f"Solution for n={n}, p={p} :")
    print(f"Best Hubs  : {best_hubs_1_based}")
    print(f"Objective  : {best_cost/1000:.2f}")
    print(f"Allocation : {', '.join(map(str, best_assignments_1_based))}")
    # print(f"Tabu list: {tabu_list}")
    # print(f"Path: {path}")
    print(f"The time use for run code in {n} node and {p} hubs is: {timee} seconds")
    
    
    with open('Solution/solution.txt', 'a') as file:
        file.write(f"Solution for n={n}, p={p} :\n")
        file.write(f"Best Hubs  : {', '.join(map(str, best_hubs_1_based))}\n")
        file.write(f"Objective  : {best_cost/1000:.2f}\n")
        file.write(f"Allocation : {', '.join(map(str, best_assignments_1_based))}\n")
        file.write(f"The time use for run code in {n} node and {p} hubs is: {timee:.2f} seconds\n")
        file.write(f"Path       : {', '.join(map(str, path))}")
        file.write(f"\n")
        file.write(f"\n")
    print(f"Done {n} nodes and {p} hub")
