import matplotlib.pyplot as plt
import numpy as np
import os
import re

def read_pareto_data(filename):
    with open(filename, 'r') as f:
        content = f.read()

    data = {}
    solutions = content.split("Solution")[1:]  # Skip the first empty element
    for solution in solutions:
        match = re.search(r'for n=(\d+), p=(\d+)', solution)
        if match:
            n = int(match.group(1))
            p = int(match.group(2))
            
            pareto_match = re.search(r'Pareto: (\[\(.*?\)\])', solution)
            if pareto_match:
                pareto_str = pareto_match.group(1)
                pareto_front = eval(pareto_str)
                
                costs = [solution[0] / 100 for solution in pareto_front]  # Divide cost by 100
                times = [solution[1] for solution in pareto_front]
                
                key = f'n={n}, p={p}'
                data[key] = {'costs': costs, 'times': times}
    
    return data

# Read data
pareto_data = read_pareto_data('output/pareto.txt')

# Extract data for n=54
p_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
cost_values = []
time_values = []

for p in p_values:
    key = f'n=54, p={p}'
    if key in pareto_data:
        cost_values.append(pareto_data[key]['costs'])
        time_values.append(pareto_data[key]['times'])
    else:
        print(f"Warning: Data missing for {key}")
        cost_values.append([])
        time_values.append([])

# Create subplots with reduced size
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Plot Total Cost
ax1.boxplot(cost_values, positions=p_values, widths=0.8, patch_artist=True,
            boxprops=dict(facecolor="orange", color="black"),
            medianprops=dict(color="black", linewidth=1.5),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5),
            showfliers=False)  # Remove outliers
ax1.set_xlabel('Number of Hubs (p)', fontsize=8)
ax1.set_ylabel('Total Cost', fontsize=8)
ax1.set_title('Deviation of Total Cost (n=54)', fontsize=10)
ax1.set_xticks(p_values)
ax1.tick_params(axis='both', which='major', labelsize=7)
ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

# Set y-axis limits for cost plot with reduced range
cost_values_flat = [val for sublist in cost_values for val in sublist if val]
if cost_values_flat:
    cost_min = np.percentile(cost_values_flat, 5)
    cost_max = np.percentile(cost_values_flat, 95)
    cost_range = cost_max - cost_min
    ax1.set_ylim(cost_min - 0.02 * cost_range, cost_max + 0.02 * cost_range)

# Plot Max Travel Time
ax2.boxplot(time_values, positions=p_values, widths=0.8, patch_artist=True,
            boxprops=dict(facecolor="blue", color="black"),
            medianprops=dict(color="black", linewidth=1.5),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5),
            showfliers=False)  # Remove outliers
ax2.set_xlabel('Number of Hubs (p)', fontsize=8)
ax2.set_ylabel('Max Travel Time', fontsize=8)
ax2.set_title('Deviation of Max Travel Time (n=54)', fontsize=10)
ax2.set_xticks(p_values)
ax2.tick_params(axis='both', which='major', labelsize=7)

# Set y-axis limits for time plot with reduced range
time_values_flat = [val for sublist in time_values for val in sublist if val]
if time_values_flat:
    time_min = np.percentile(time_values_flat, 5)
    time_max = np.percentile(time_values_flat, 95)
    time_range = time_max - time_min
    ax2.set_ylim(time_min - 0.02 * time_range, time_max + 0.02 * time_range)

# Adjust layout and reduce white space
plt.tight_layout()
plt.subplots_adjust(wspace=0.3, left=0.1, right=0.95, top=0.9, bottom=0.15)

# Create folder if it doesn't exist
if not os.path.exists('plot_deviation'):
    os.makedirs('plot_deviation')

# Save the plot with reduced size
plt.savefig('plot_deviation/deviation.png', dpi=300, bbox_inches='tight')

# Close the plot to free up memory
plt.close()
