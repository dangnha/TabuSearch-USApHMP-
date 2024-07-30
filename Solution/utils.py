import numpy as np
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import random


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

        return (N, p, alpha, delta, ksi, np.array(points), np.array(W))

# Calculate the distance
def CalDistance(coords):
    distances = np.zeros((len(coords), len(coords)))
    for i in range(len(coords)):
        for j in range(len(coords)):
            distances[i, j] = euclidean(coords[i], coords[j])
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

# Predict the best allocation
# def cal_distance(hubs, n, distances):
#     nodes = list(range(n))
    
#     for i, node in enumerate(nodes):
#         if node == hubs[0]:
#             nodes[i] = hubs[0]
#         elif node == hubs[1]:
#             nodes[i] = hubs[1]
            
#         if (distances[node, hubs[0]] + distances[hubs[0], node]) < (distances[node, hubs[1]] + distances[hubs[1], node]):
#             nodes[i] = hubs[0]
#         elif (distances[node, hubs[0]] + distances[hubs[0], node]) > (distances[node, hubs[1]] + distances[hubs[1], node]):
#             nodes[i] = hubs[1]
#     return nodes
            
# Generate robust solution
def get_initial_solution_robust(n, p, weights, distances):
    potential_hub = cal_weights(n, weights)
    hubs = sorted(potential_hub, key=potential_hub.get)[:p]
    
    # allocation = cal_distance(hubs, n, distances)
    allocation = [min(hubs, key=lambda x: distances[i][x]) for i in range(n)]
    return hubs, allocation


# Objective function
def calculate_total_cost(assignments, n, weights, distances, alpha, delta, ksi):    
    total_cost = 0
    for i in range(n):
        for j in range(n):
                k = assignments[i]
                l = assignments[j]
                total_cost += weights[i, j] * (delta * distances[i, k] + alpha * distances[k, l] + ksi * distances[l, j])
    return total_cost


# # Neighborhood function
# def get_neighborhood(hubs, n, distances):
#     neighborhood = []
#     for i in range(n):
#         if i not in hubs:
#             for hub in hubs:
#                 new_hubs = hubs.copy()
#                 new_hubs.remove(hub)
#                 new_hubs.append(i)
#                 new_assignments =  [random.choice(new_hubs) for _ in range(n)]
#                 neighborhood.append((new_hubs, new_assignments))
#     return neighborhood

from queue import PriorityQueue




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


def tabu_search(tabu_tenure, n, p, weights, distances, alpha, delta, ksi):
    best_hubs, best_assignments = get_initial_solution_robust(n, p, weights, distances)
    best_cost = calculate_total_cost(best_assignments, n, weights, distances, alpha, delta, ksi)
    current_hubs, current_assignments = best_hubs, best_assignments
    tabu_list = []
    iteration = 0
    # max_iterations = 100
    
    if n <= 20:
        max_iterations = 10
    elif n == 30:
        max_iterations = 15
    elif n == 40:
        max_iterations = 20
    elif n > 40:
        max_iterations = 30
    
    
    path = []

    while iteration < max_iterations: # 100
        neighborhood = get_neighborhood(current_hubs, n, distances)
        best_candidate_hubs, best_candidate_assignments = None, None
        best_candidate_cost = float('inf')

        # Explore the neighborhood (p*N)
        for candidate_hubs, candidate_assignments in neighborhood:
            if (candidate_hubs, candidate_assignments) not in tabu_list:
                candidate_cost = calculate_total_cost(candidate_assignments, n, weights, distances, alpha, delta, ksi)
                if candidate_cost < best_candidate_cost:
                    best_candidate_hubs, best_candidate_assignments = candidate_hubs, candidate_assignments
                    best_candidate_cost = candidate_cost

        # Update the best solution found
        if best_candidate_cost < best_cost:
            best_hubs, best_assignments = best_candidate_hubs, best_candidate_assignments
            best_cost = best_candidate_cost

        # Move to the best candidate solution
        current_hubs, current_assignments = best_candidate_hubs, best_candidate_assignments

        # Add current solution to the tabu list
        tabu_list.append((current_hubs, current_assignments, best_cost))
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)  # Remove oldest entry if tabu list exceeds its tenure

        # Increment iteration count
        iteration += 1

        path.append((best_candidate_hubs, best_candidate_assignments))
        #     print(f"Iteration {iteration}, Best Cost: {best_cost}, Current: {current_assignments}, Best assignments {best_assignments}")

    return best_hubs, best_assignments, best_cost, path


def find_best_allocation():
    pass


# Plot the nodes and the assignment
def plot_solution(coords, hubs, assignments):
    plt.figure(figsize=(20, 16))
    for i, coord in enumerate(coords):
        plt.scatter(coord[0], coord[1], color='blue' if i not in hubs else 'red', s=100)
        plt.text(coord[0], coord[1], f'{i + 1}', fontsize=12, ha='right')

        if i not in hubs:
            assigned_hub = assignments[i]
            plt.plot([coord[0], coords[assigned_hub][0]], [coord[1], coords[assigned_hub][1]], 'gray', linestyle='--')

    # Connect the hub nodes
    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            plt.plot([coords[hubs[i]][0], coords[hubs[j]][0]], [coords[hubs[i]][1], coords[hubs[j]][1]], 'red', linestyle='-', linewidth=2)

    plt.title('USApHMP Solution')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()