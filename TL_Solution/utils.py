import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import random
from math import radians, sin, cos, sqrt, atan2

# data

def parse_input(filepath, dataset):
    if dataset == 'AP':
        return parse_AP(filepath)
    else:
        raise ValueError("Unknown dataset. Supported datasets: \
                         'AP' (\"Australia Post\" dataset)")
    
def parse_AP(filepath):
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        # read lines ignoring empty
        lines = [line for line in file.readlines() if line.strip()]

        # first line contains parameters of the problem
        N = int(lines[0])
        
        # next num_nodes lines contain num_nodes points
        points = []
        for line in lines[1:N+1]:
            points.append(tuple(map(float, line.split())))
        
        # next N lines contain NxN matrix containing flows between points
        W = []
        for line in lines[N+1:2*N+1]:
            W.append(list(map(float, line.split())))

        p = int(lines[2*N+1])
        delta = float(lines[2*N+2])
        alpha = float(lines[2*N+3])
        ksi = float(lines[2*N+4])
        beta = float(lines[2*N+5])
        
        capacity = []
        for line in lines[2*N+6:3*N+6]:
            capacity.append(float(line))
        capacity_array = np.array(capacity)

        return (N, p, alpha, delta, ksi, np.array(points), np.array(W), beta, capacity_array)

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    # Radius of Earth in kilometers
    R = 6371.0
    distance = R * c
    return distance

# Calculate the distance
def CalDistance(coords):
    num_coords = len(coords)
    distances = np.zeros((num_coords, num_coords))
    for i in range(num_coords):
        for j in range(num_coords):
            if i != j:  # Avoid computing distance for the same point
                distances[i, j] = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
    return distances

# Generate initial solution
def generate_initial_solution(num_nodes, p):
    hubs = random.sample(range(num_nodes), p)
    assignments = [random.choice(hubs) for _ in range(num_nodes)]
    return hubs, assignments

# Make the top hub
def cal_weights(n, weights):
    potential_hub = {}
    nodes = list(range(n))
    for node in nodes:
        potential_hub[node] = np.sum(weights[:, node]) + np.sum(weights[node, :])
    return potential_hub

            
# Generate robust solution
def get_initial_solution_robust(n, p, weights, distances):
    potential_hub = cal_weights(n, weights)
    hubs = sorted(potential_hub, key=potential_hub.get)[:p]
    # allocation = cal_distance(hubs, n, distances)
    allocation = [min(hubs, key=lambda x: distances[i][x]) for i in range(n)]
    return hubs, allocation


# Objective function
def calculate_total_cost(assignments, n, weights, distances, alpha, delta, ksi, beta, capacity):    
    cost = calculate_cost(assignments, n, weights, distances, alpha, delta, ksi, capacity)
    time = calculate_time(assignments, n, weights, distances, beta)
    return cost, time

# def calculate_cost(assignments, n, weights, distances, alpha, delta, ksi, capacity):    
#     total_cost = 0

#     for i in range(n):
#         for j in range(n):
#             k = assignments[i]
#             l = assignments[j]
#             total_cost += weights[i, j] * (ksi * distances[i, k] + alpha * distances[k, l] + delta * distances[l, j])
    
#     return total_cost

def calculate_cost(assignments, n, weights, distances, alpha, delta, ksi, capacity):
    total_cost = 0
    # capacity_violation_penalty = 1e8  # Large penalty for capacity violation

    for i in range(n):
        for j in range(n):
            k = assignments[i]
            l = assignments[j]
            total_cost += weights[i, j] * (ksi * distances[i, k] + alpha * distances[k, l] + delta * distances[l, j])
    # Check capacity constraints
    # outgoing_weight = np.zeros(n)
    # incoming_weight = np.zeros(n)

    # for i in range(n):
    #     for j in range(n):
    #         outgoing_weight[assignments[i]] += weights[i, j]
    #         incoming_weight[assignments[j]] += weights[i, j]

    # for hub in set(assignments):
    #     if outgoing_weight[hub] > capacity[hub] or incoming_weight[hub] > capacity[hub]:
    #         total_cost += capacity_violation_penalty

    return total_cost

def calculate_time(assignments, n, weights, travel_times, beta):
    max_time = 0
    for i in range(n):
        for j in range(n):
            k = assignments[i]
            l = assignments[j]
            if assignments[i] == k and assignments[j] == l:
                time_ik = travel_times[i][k]
                time_lj = travel_times[l][j]
                transhipment_time = beta * travel_times[k][l] + 20
                total_time = time_ik + time_lj + transhipment_time
                
                if total_time > max_time:
                    max_time = total_time
    return max_time


def dominates(sol1, sol2):
    cost1, time1 = sol1
    cost2, time2 = sol2
    return (cost1 <= cost2 and time1 < time2) or (cost1 < cost2 and time1 <= time2)


def get_neighborhood(hubs, n, distances):
    neighborhood = []
    hub_set = set(hubs)
    non_hubs = list(set(range(n)) - hub_set)
    
    for hub in hubs:
        for non_hub in non_hubs:
            new_hubs = hubs.copy()
            new_hubs.remove(hub)
            new_hubs.append(non_hub)
            
            # Create new assignments based on the new hubs
            new_assignments = [min(new_hubs, key=lambda x: distances[i][x]) for i in range(n)]
            
            neighborhood.append((new_hubs, new_assignments))
    
    return neighborhood


def plot_solution(coords, hubs, assignments):
    plt.figure(figsize=(20, 16))
    for i, coord in enumerate(coords):
        plt.scatter(coord[0], coord[1], color='blue' if i not in hubs else 'red', s=100)
        plt.text(coord[0], coord[1], f'{i + 1}', fontsize=12, ha='right')

        if i not in hubs:
            assigned_hub = assignments[i]
            plt.plot([coord[0], coords[assigned_hub][0]], [coord[1], coords[assigned_hub][1]], 'gray', linestyle='--')

    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            plt.plot([coords[hubs[i]][0], coords[hubs[j]][0]], [coords[hubs[i]][1], coords[hubs[j]][1]], 'red', linestyle='-', linewidth=2)

    plt.title('USApHMP Solution')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()
    
    
    
def array_in_list(array, list_of_arrays):
    return any(np.array_equal(array, x) for x in list_of_arrays)

def dominates_sol(candidate, current):
    return (candidate[0] < current[0] and candidate[1] <= current[1]) or (candidate[0] <= current[0] and candidate[1] < current[1])

def remove_dominated_solutions(solutions):
    non_dominated = []
    for candidate in solutions:
        dominated = False
        to_remove = []
        for other in non_dominated:
            if dominates_sol(candidate, other):
                to_remove.append(other)
            elif dominates_sol(other, candidate):
                dominated = True
                break
        if not dominated:
            non_dominated.append(candidate)
        for sol in to_remove:
            non_dominated.remove(sol)
    return non_dominated

def tabu_search(tabu_tenure, n, p, weights, distances, alpha, delta, ksi, beta, capacity):
    best_hubs, best_assignments = get_initial_solution_robust(n, p, weights, distances)
    best_cost, best_time = calculate_total_cost(best_assignments, n, weights, distances, alpha, delta, ksi, beta, capacity)
    tabu_list = []
    pareto_front = [[(best_cost, best_time, best_hubs, best_assignments)]]
    iteration = 0
    
    max_iterations = 15 if n > 40 else 5
    count_pareto = []  # Initialize count_pareto list
    
    # Initialize lists to store best cost and time for each iteration
    best_costs = [best_cost]
    best_times = [best_time]

    while iteration < max_iterations:
        pre_non_dominated_list = pareto_front[-1]
        new_pareto_front = []
        for current_cost, current_time, current_hubs, _ in pre_non_dominated_list:
            neighborhood = get_neighborhood(current_hubs, n, distances)
            non_dominated_neighbor = []
            
            for candidate_hubs, candidate_assignments in neighborhood:
                if not array_in_list((candidate_hubs, candidate_assignments), tabu_list):
                    candidate_cost, candidate_time = calculate_total_cost(candidate_assignments, n, weights, distances, alpha, delta, ksi, beta, capacity)
                    
                    if dominates((candidate_cost, candidate_time), (current_cost, current_time)):
                        new_solution = (candidate_cost, candidate_time, candidate_hubs, candidate_assignments)
                        non_dominated_neighbor.append(new_solution)

            # Append non-dominated neighbors to new_pareto_front
            new_pareto_front.extend(non_dominated_neighbor)
        
        new_pareto_front = remove_dominated_solutions(new_pareto_front)
        
        for solution in new_pareto_front:
            candidate_hubs, candidate_assignments = solution[2], solution[3]
            tabu_list.append((candidate_hubs, candidate_assignments))
            
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
        
        iteration += 1
        if new_pareto_front:
            pareto_front.append(new_pareto_front)
            
            # Update best cost and time for this iteration
            iteration_best_cost = min(solution[0] for solution in new_pareto_front)
            iteration_best_time = min(solution[1] for solution in new_pareto_front)
            best_costs.append(min(best_costs[-1], iteration_best_cost))
            best_times.append(min(best_times[-1], iteration_best_time))
        else:
            # If no new solutions, keep the previous best
            best_costs.append(best_costs[-1])
            best_times.append(best_times[-1])
            
        count_pareto.append(len([item for sublist in pareto_front for item in sublist]))
        
    return pareto_front, count_pareto, best_costs, best_times