import matplotlib.pyplot as plt
import re

# Read the content of the file
with open('output/pareto_iteration.txt', 'r') as file:
    content = file.read()

# Extract data using regular expressions
pattern = r'n=(\d+), p=(\d+): \[([\d, ]+)\]'
matches = re.findall(pattern, content)

# Process and plot each dataset
for match in matches:
    n, p, data_str = match
    data = [int(x) for x in data_str.split(', ')]
    
    plt.figure(figsize=(14, 8))
    plt.plot(range(1, len(data) + 1), data, marker='o')
    plt.title(f'Size of Pareto Front over Iterations (n={n}, p={p})')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Size of Pareto Front')
    plt.grid(True)
    
    # Ensure y-axis starts from 0 and has integer ticks with step of 2
    plt.ylim(bottom=0)
    plt.yticks(range(0, max(data) + 2, 2))
    # Create folder if it doesn't exist
    import os
    if not os.path.exists('pareto_iteration_plot'):
        os.makedirs('pareto_iteration_plot')
    
    # Save the plot
    plt.savefig(f'pareto_iteration_plot/pareto_iteration_plot_n{n}_p{p}.png')
    plt.close()

print("Plots have been generated and saved in the 'output' folder.")
