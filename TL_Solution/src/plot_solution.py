import matplotlib.pyplot as plt

with open('plot_sol_iter/solutions.txt', 'r') as file:
    data = eval(file.read())
    
for case in data:
    n = case["n"]
    p = case["p"]
    sol = case["solutions"]
    
    # Extract iterations and number of solutions
    iterations = [pair[0] for pair in sol]
    num_solutions = [pair[1] for pair in sol]
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, num_solutions, marker='o')
    
    # Add labels and title
    plt.xlabel('Iteration')
    plt.ylabel('Number of Solutions')
    plt.title(f'Number of Solutions per Iteration (n={n}, p={p})')
    
    # Add total solutions text
    total_solutions = sum(num_solutions)
    plt.text(0.02, 0.98, f'Total Solutions: {total_solutions}', 
             transform=plt.gca().transAxes, 
             verticalalignment='top')
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save the plot
    plt.savefig(f'plot_sol_iter/solutions_n{n}_p{p}.png')
    plt.close()