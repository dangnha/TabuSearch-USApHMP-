import matplotlib.pyplot as plt
import numpy as np
import os
import re

def read_performance_data(filename):
    with open(filename, 'r') as f:
        content = f.read()

    data = {}
    solutions = content.split("\n\n")
    for solution in solutions:
        if solution.strip():
            match = re.search(r'n=(\d+), p=(\d+)', solution)
            if match:
                n = int(match.group(1))
                p = int(match.group(2))
                
                values = re.findall(r'\d+\.\d+', solution)
                values = [float(v) for v in values]
                
                key = f'n={n}, p={p}'
                data[key] = values
    
    return data

def plot_performance(cost_data, time_data):
    for key in cost_data.keys():
        if key in time_data:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
            
            iterations = range(1, len(cost_data[key]) + 1)
            
            # Plot Total Cost (divided by 100)
            ax1.plot(iterations, [cost/100 for cost in cost_data[key]], color='blue', marker='o')
            ax1.set_xlabel('Iteration')
            ax1.set_ylabel('Total Cost')
            ax1.set_title(f'Total Cost Performance ({key})')
            ax1.grid(True)
            
            # Plot Max Travel Time
            ax2.plot(iterations, time_data[key], color='red', marker='s')
            ax2.set_xlabel('Iteration')
            ax2.set_ylabel('Max Travel Time')
            ax2.set_title(f'Max Travel Time Performance ({key})')
            ax2.grid(True)
            
            plt.tight_layout()
            
            # Create folder if it doesn't exist
            if not os.path.exists('performance_plots'):
                os.makedirs('performance_plots')
            
            # Save the plot
            plt.savefig(f'performance_plots/performance_{key.replace("=", "_")}.png')
            plt.close()
        else:
            print(f"Warning: Key '{key}' not found in time_data")

# Read data
cost_data = read_performance_data('output/best_cost_iteration.txt')
time_data = read_performance_data('output/best_time_iteration.txt')

# Plot performance
plot_performance(cost_data, time_data)
