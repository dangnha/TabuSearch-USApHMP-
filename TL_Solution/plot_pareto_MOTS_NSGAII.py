import matplotlib.pyplot as plt
import os
from data import initial_coords
import re

def read_box_plot_data(filename):
    solutions = {}
    current_n_p = None
    
    with open(filename, 'r') as file:
        content = file.readlines()
        
    for line in content:
        if line.startswith('Pareto Frontier(n='):
            # Extract n and p values
            match = re.search(r'n=(\d+), p=(\d+)', line)
            if match:
                n = int(match.group(1))
                p = int(match.group(2))
                current_n_p = (n,p)
                solutions[current_n_p] = []
        elif line.startswith('Solution:') and current_n_p:
            # Extract cost and time from next lines
            cost_line = next((l for l in content[content.index(line)+1:] if 'Cost of solutions:' in l), None)
            time_line = next((l for l in content[content.index(line)+1:] if 'Time of solutions:' in l), None)
            hubs_line = next((l for l in content[content.index(line)+1:] if 'Hubs:' in l), None)
            
            if cost_line and time_line and hubs_line:
                cost = float(cost_line.split(':')[1].strip())
                time = float(time_line.split(':')[1].strip())
                hubs = eval(hubs_line.split(':')[1].strip())
                solutions[current_n_p].append((cost, time, hubs))
                
    return solutions

box_plot_solutions = read_box_plot_data('box_plot_data.txt')

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
                x_coords_box = []
                y_coords_box = []

                # Plot NSGA-II solutions
                for solution in pareto_front:
                    cost, time_metric, hubs, assignments = solution
                    hubs = [h + 1 for h in hubs]
                    assignments = [a + 1 for a in assignments]
                    
                    x_coords.append(time_metric)
                    y_coords.append(cost/100)
                    
                    plt.scatter(time_metric, cost/100, marker='^', color='darkblue', s=200, edgecolors='red')
                    plt.text(time_metric, cost/100, str(hubs), fontsize=14, ha='center')

                # Plot box plot solutions if available
                if (n,p) in box_plot_solutions:
                    for cost, time, hubs in box_plot_solutions[(n,p)]:
                        x_coords_box.append(time)
                        y_coords_box.append(cost)
                        plt.scatter(time, cost, marker='o', color='green', s=200, edgecolors='black')
                        plt.text(time, cost, str(hubs), fontsize=14, ha='center')

                # Sort and plot NSGA-II line
                sorted_points = sorted(zip(x_coords, y_coords), key=lambda x: x[0])  # Sort by x (time) instead of y
                sorted_x, sorted_y = zip(*sorted_points)
                plt.plot(sorted_x, sorted_y, color='red', linestyle='--', linewidth=1, label='MOTS')

                # Sort and plot box plot line
                if x_coords_box:
                    sorted_points_box = sorted(zip(x_coords_box, y_coords_box), key=lambda x: x[0])  # Sort by x (time) instead of y
                    sorted_x_box, sorted_y_box = zip(*sorted_points_box)
                    plt.plot(sorted_x_box, sorted_y_box, color='green', linestyle='--', linewidth=1, label='NSGA-II')

                plt.xlabel('Max Travel Time', fontsize=14)
                plt.ylabel('Travel Cost', fontsize=14)
                plt.title(f'Pareto Plot for n={n}, p={p}', fontsize=16)
                plt.legend(fontsize=12)

                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.gca().get_xaxis().get_major_formatter().set_scientific(False)

                plt.grid(True)

                output_folder = 'pareto_plots_MOTS_NSGAII'
                os.makedirs(output_folder, exist_ok=True)
                filename = f'pareto_plot_n{n}_p{p}.png'
                filepath = os.path.join(output_folder, filename)
                plt.savefig(filepath)
                plt.close()