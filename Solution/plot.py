from data import initial_coords
from utils import plot_solution
import matplotlib
import matplotlib.pyplot as plt
import ast
import os


blocks = []
with open('Solution/solution.txt', 'r') as file:
    lines = file.readlines()

    # Temporary variables to store current block's data
    current_block = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith("Solution for n="):
            if current_block:
                blocks.append(current_block)
            current_block = {'n': None, 'p': None, 'hubs': None, 'assignments': None, 'steps': None}
            current_block['n'] = int(line.split('=')[1].split(',')[0].strip())
            current_block['p'] = int(line.split('=')[2].split(':')[0].strip())
        elif line.startswith("Best Hubs  :"):
            try:
                current_block['hubs'] = list(map(int, line.split(':')[1].strip().split(', ')))
            except ValueError as e:
                print(f"Error parsing hubs: {line}")
                print(f"Exception: {e}")
        elif line.startswith("Allocation :"):
            try:
                current_block['assignments'] = list(map(int, line.split(':')[1].strip().split(', ')))
            except ValueError as e:
                print(f"Error parsing assignments: {line}")
                print(f"Exception: {e}")
        elif line.startswith("Path       :"):
            try:
                path = line.split(':')[1].strip()
                current_block['steps'] = ast.literal_eval(f"[{path}]")
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing path: {line}")
                print(f"Exception: {e}")
    
    # Append the last block
    if current_block:
        blocks.append(current_block)

# Plot each block
matplotlib.use('Agg')
def visualize(blocks):
    for idx, block in enumerate(blocks):
        steps = block['steps']
        hubs = block['hubs']
        assignments = block['assignments']
        
        coords = initial_coords(len(assignments), len(hubs))
        
        # Create output directory
        output_folder = f'Solution/Visualize/{len(assignments)}-{len(hubs)}'
        os.makedirs(output_folder, exist_ok=True)
        
        for i, (hubs_step, assignments_step) in enumerate(steps):
            plot_solution(coords, hubs_step, assignments_step)
            plt.savefig(os.path.join(output_folder, f'step_{i}.png'))
            plt.close()

visualize(blocks)
