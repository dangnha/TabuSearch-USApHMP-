import time
from utils import tabu_search, plot_solution, remove_dominated_solutions
from data import initial_parameter
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker

# experements = ["10.2", "10.3", "10.4", "20.2", "20.3", "20.4", "40.2", "40.3", "40.4", "50.2", "50.3", "50.4", "100.2", "100.3", "100.4"]
experements = ["10.2", "10.3", "10.4", "10.5", "54.2", "54.3", "54.4", "54.5", "54.6", "54.7", "54.8", "54.9", "54.10",]

for file_db in experements:
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
        pareto_front = tabu_search(tabu_tenure, n, p, weights, distances, alpha, delta, ksi, beta, capacity)
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

    with open('pareto.txt', 'a') as file:
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
    
    # print(pareto_front)

    # Your code
    # x_coords = [item[1] for item in pareto_front]
    # y_coords = [item[0]/100 for item in pareto_front]
    # labels = [item[2] for item in pareto_front]
    # for allocation in range(len(labels)):
    #     for node in range(len(labels[allocation])):
    #         labels[allocation][node] += 1

    # # Create the scatter plot
    # plt.figure(figsize=(20, 18))
    # plt.scatter(x_coords, y_coords)

    # # Add labels to the points
    # for i, label in enumerate(labels):
    #     plt.text(x_coords[i], y_coords[i], str(label), fontsize=9, ha='right')

    # # Set the labels for the axes
    # plt.xlabel('Max Travel Time')
    # plt.ylabel('Travel Cost')
    # plt.title('Scatter Plot with Labels')

    # # Disable scientific notation on the x-axis
    # plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    # plt.gca().get_xaxis().get_major_formatter().set_scientific(False)

    # # Display the plot
    # plt.grid(True)
    # plt.show()
    
    
    # # Define the folder and file name
    # folder = 'patero_visualize'  # Replace with your desired folder path
    # file_name = f'scatter_plot{n}-{p}.png'

    # # Create the folder if it doesn't exist
    # os.makedirs(folder, exist_ok=True)

    # # Save the plot
    # file_path = os.path.join(folder, file_name)
    # plt.savefig(file_path)
