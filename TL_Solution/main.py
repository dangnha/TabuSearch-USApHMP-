import time
from utils import tabu_search, plot_solution, remove_dominated_solutions
from data import initial_parameter
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker



with open('hub_node.txt', 'r') as file:
    experiments = eval(file.read().strip())
# experiments = ["10.2", "10.3", "10.4", "10.5", "54.2", "54.3", "54.4", "54.5", "54.6", "54.7", "54.8", "54.9", "54.10",]
print("Running Successfully! Please wait a moment...")

for file_db in experiments:
    n, p, alpha, delta, ksi, coords, weights, distances, beta, capacity = initial_parameter(file_db)
    tabu_tenure = 50

    # distances = """0.00000	4.68000	7.38500	12.86100	17.67300	22.22000	29.36600	36.07600	44.14600	50.09300
    # 4.68000	0.00000	2.70800	8.19800	13.02100	17.57900	24.68600	31.41500	39.52700	45.49500
    # 7.38500	2.70800	0.00000	5.49400	10.32200	14.88300	21.98200	28.74000	36.89200	42.87900
    # 12.86100	8.19800	5.49400	0.00000	4.83000	9.39400	16.54300	23.43600	31.71400	37.74500
    # 17.67300	13.02100	10.32200	4.83000	0.00000	4.96400	12.25100	19.32400	27.73200	33.79700
    # 22.22000	17.57900	14.88300	9.39400	4.96400	0.00000	8.02500	15.31100	23.82700	29.90000
    # 29.36600	24.68600	21.98200	16.54300	12.25100	8.02500	0.00000	7.33500	15.86800	21.92800
    # 36.07600	31.41500	28.74000	23.43600	19.32400	15.31100	7.33500	0.00000	8.53200	14.59600
    # 44.14600	39.52700	36.89200	31.71400	27.73200	23.82700	15.86800	8.53200	0.00000	6.07500
    # 50.09300	45.49500	42.87900	37.74500	33.79700	29.90000	21.92800	14.59600	6.07500	0.00000
    # """
    # distances = list(map(float, distances.split()))
    # distances = np.array(distances).reshape(10, 10)

    times = []
    costs = []
    time_metrics = []
    solutions_cost = {}
    solutions_time = {}
    iterations = 0

    # Determine the number of iterations based on n
    if n <= 20:
        iterations = 20
    elif n == 30:
        iterations = 10
    elif n == 40:
        iterations = 5
    elif n > 40:
        iterations = 1

    # Run the Tabu Search for the specified number of iterations
    for i in range(iterations):
        start_time = time.time()
        pareto_front, count_pareto, best_costs, best_times = tabu_search(tabu_tenure, n, p, weights, distances, alpha, delta, ksi, beta, capacity)
        end_time = time.time()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        pareto_front = [item for sublist in pareto_front for item in sublist]
        
        # Costtttttttttttttttttt
        for solution in pareto_front:
            cost, time_metric, hubs, assignments = solution
            costs.append(cost)
            solutions_cost[cost] = (hubs, assignments, time_metric)
            
        # Timeeeeeeeeeeeeeeeeeee
        # for solution in pareto_front:
        #     cost, time_metric, hubs, assignments = solution
        #     time_metrics.append(time_metric)
        #     solutions_time[time_metric] = (hubs, assignments, cost)

    # Find the best solution based on cost
    best_cost = min(costs)
    best_hubs_cost, best_assignments_cost, best_time_metric_cost = solutions_cost[best_cost]
    min_time = min(times)
    
    # =================================================================================================
    # Find the best solution based on time
    # best_time_metric = min(time_metrics)
    # best_hubs_times, best_assignments_times, best_cost_times = solutions_time[time_metric]
    


    # Convert best_assignments to 1-based index for clearer output
    best_assignments_1_based = [x + 1 for x in best_assignments_cost]
    best_hubs_1_based = [x + 1 for x in best_hubs_cost]

    # Output the results
    print(f"Solution for n={n}, p={p} :")
    print(f"Best Hubs  : {best_hubs_1_based}")
    print(f"Best Total Cost  : {best_cost/100:.2f}")
    print(f"Best Max Travel Time : {best_time_metric_cost}")
    # print(f"Allocation : {', '.join(map(str, best_assignments_1_based))}")
    print(f"The time used for running the code in {n} nodes and {p} hubs is: {min_time:.2f} seconds")
    # plot_solution(coords, best_hubs, best_assignments)

    # Create output folder if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    with open('output/pareto.txt', 'a') as file:
        file.write(f"Solution for n={n}, p={p} :\n")
        # file.write(f"Best Hubs  : {', '.join(map(str, best_hubs_1_based))}\n")
        # file.write(f"Best Total Cost  : {best_cost/100:.2f}\n")
        # file.write((f"Best Max Travel Time : {best_time_metric_cost:.2f} \n"))
        # file.write(f"Allocation : {', '.join(map(str, best_assignments_1_based))}\n")
        # file.write(f"The time used for running the code in {n} nodes and {p} hubs is: {min_time:.2f} seconds\n")
        # file.write(f"Patero collection: {pareto_front}\n")
        file.write(f"Pareto: {remove_dominated_solutions(pareto_front)}")
        file.write("\n")
        file.write("\n")
        
    with open('output/solution.txt', 'a') as file:
        file.write(f"Solution for n={n}, p={p} :\n")
        file.write(f"Best Hubs  : {', '.join(map(str, best_hubs_1_based))}\n")
        file.write(f"Best Total Cost  : {best_cost/100:.2f}\n")
        file.write((f"Best Max Travel Time : {best_time_metric_cost:.2f} \n"))
        file.write(f"The time used for running the code in {n} nodes and {p} hubs is: {min_time:.2f} seconds\n")
        file.write("\n")
        file.write("\n")
    
    with open('output/pareto_iteration.txt', 'a') as file:
        file.write(f"Number of elements in Pareto Front of solution for n={n}, p={p}: {count_pareto}")
        file.write("\n")
        file.write("\n")
        
    with open('output/best_cost_iteration.txt', 'a') as file:
        file.write(f"Best Cost of Pareto Front of solution for n={n}, p={p}: {best_costs}")
        file.write("\n")
        file.write("\n")
    
    with open('output/best_time_iteration.txt', 'a') as file:
        file.write(f"Best Time of Pareto Front of solution for n={n}, p={p}: {best_times}")
        file.write("\n")
        file.write("\n")
    

# Run all plot files
import subprocess
import os

plot_files = [
    'plot_performance.py',
    'plot_box.py',
    'plot_pareto.py',
    'plot_iteration.py'
]

for plot_file in plot_files:
    try:
        subprocess.run(['python', plot_file], check=True)
        print(f"Successfully ran {plot_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {plot_file}: {e}")
    except FileNotFoundError:
        print(f"File not found: {plot_file}")

print("All plot files have been executed.")