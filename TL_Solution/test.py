import numpy as np
from data import initial_parameter

n, p, alpha, delta, ksi, coords, weights, distances, beta = initial_parameter("10.2")

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

a = calculate_time([0, 0, 0, 5, 5, 5, 5, 5, 5, 5], n, weights, distances, beta)
print(a)

def calculate_cost(assignments, n, weights, distances, alpha, delta, ksi):    
    total_cost = 0
    for i in range(n):
        for j in range(n):
                k = assignments[i]
                l = assignments[j]
                total_cost += weights[i, j] * (ksi * distances[i, k] + alpha * distances[k, l] + delta * distances[l, j])
    return total_cost

b = calculate_cost([0, 0, 0, 5, 5, 5, 5, 5, 5, 5], n, weights, distances, alpha, delta, ksi)
print(b)


