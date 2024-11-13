import matplotlib.pyplot as plt
import os
from data import initial_coords
import re

with open('output/pareto.txt', 'r') as file:
    content = file.read()
    solutions = content.split("Solution")[1:]  # Skip the first empty element
    processed_solutions = []
    for solution in solutions:
        match = re.search(r'for n=(\d+), p=(\d+)', solution)
        if match:
            n = int(match.group(1))
            p = int(match.group(2))
            coords = initial_coords(n, p)
            
            pareto_match = re.search(r'Pareto: (\[\(.*?\)\])', solution)
            if pareto_match:
                pareto_str = pareto_match.group(1)
                pareto_front = eval(pareto_str)
                
                plt.figure(figsize=(18, 10))
                x_coords = []
                y_coords = []
                for solution in pareto_front:
                    cost, time_metric, hubs, assignments = solution
                    hubs = [h + 1 for h in hubs]
                    assignments = [a + 1 for a in assignments]
                    
                    x_coords.append(time_metric)
                    y_coords.append(cost/100)
                    
                    
                    plt.scatter(time_metric, cost/100, marker='^', color='darkblue', s=250, edgecolors='red')
                    plt.text(time_metric, cost/100, str(hubs), fontsize=16, ha='right')
                    # plt.scatter(time_metric, cost/100, marker='o', color='green', s=250, edgecolors='black', alpha=0.7)
                    # plt.text(time_metric, cost/100, str(hubs), fontsize=14, ha='right', va='bottom', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

                # Sort the points by y-coordinate (cost) in descending order
                sorted_points = sorted(zip(x_coords, y_coords), key=lambda x: x[1], reverse=True)
                sorted_x, sorted_y = zip(*sorted_points)

                # Connect the points with a red dashed line from top to bottom
                plt.plot(sorted_x, sorted_y, color='red', linestyle='--', linewidth=1)

                plt.xlabel('Max Travel Time', fontsize=14)
                plt.ylabel('Travel Cost', fontsize=14)
                plt.title(f'Pareto Plot for n={n}, p={p}', fontsize=16)

                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.gca().get_xaxis().get_major_formatter().set_scientific(False)

                plt.grid(True)

                output_folder = 'pareto_plots_conference'
                os.makedirs(output_folder, exist_ok=True)
                filename = f'pareto_plot_n{n}_p{p}.png'
                filepath = os.path.join(output_folder, filename)
                plt.savefig(filepath)
                plt.close()