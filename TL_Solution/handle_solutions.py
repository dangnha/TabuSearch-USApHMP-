import os

with open('output/number_of_generating_solutions_iteration.txt', 'r') as file:
    number_of_generating_solutions = file.read()

    # Split the content by newlines and process each line
    lines = number_of_generating_solutions.strip().split('\n\n')
    # Initialize list to store the processed data
    solutions_data = []
    
    # Process each line
    for i in range(0, len(lines)):
        line = lines[i]
        if line.startswith("Number of generating solutions of Pareto Front of solution for"):
            # Extract n and p values
            n_p_part = line.split("n=")[1].split(",")[0]
            p_part = line.split("p=")[1].split(":")[0]
            n = int(n_p_part)
            p = int(p_part)
            
            # Extract the solutions list
            solutions_list = eval(line.split(": ")[1])
            
            solutions_data.append({
                'n': n,
                'p': p,
                'solutions': solutions_list
            })

result = []
                
for case in solutions_data:
    sol_each_case = []
    n = case["n"]
    p = case["p"]
    solutions_list = case["solutions"]
    
    for iter, generating_solutions in enumerate(solutions_list):
        print(iter, generating_solutions)
        exit()
        sol_each_case.append([iter, len(generating_solutions)])
    result.append({
        "n": n,
        "p": p,
        "solutions": sol_each_case,
    })
    
# Create plot_sol_iter directory if it doesn't exist
if not os.path.exists('plot_sol_iter'):
    os.makedirs('plot_sol_iter')

# Write result to solutions.txt file
with open('plot_sol_iter/solutions.txt', 'w') as file:
    file.write(str(result))