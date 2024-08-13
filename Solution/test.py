from data import initial_parameter
n, p, alpha, delta, ksi, coords, weights, distances = initial_parameter()
tabu_tenure = 10

def calculate_total_cost(assignments, n, weights, distances, alpha, delta, ksi):
    total_cost = 0
    for i in range(n):
        for j in range(n):
                k = assignments[i]
                l = assignments[j]
                total_cost += weights[i, j] * (delta * distances[i, k] + alpha * distances[k, l] + ksi * distances[l, j])
    return total_cost

a = calculate_total_cost([2, 3, 2, 3, 6, 3, 6, 6, 6, 6], n, weights, distances, alpha, delta, ksi)


def cost(chromosome, distance, weights):
    total_cost = 0
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            total_cost += weights[i][j] * (3 * distance[i][chromosome[i]] + 0.75*distance[chromosome[i]][chromosome[j]] + 2 * distance[chromosome[j]][j])
    return total_cost
b = cost([2, 3, 2, 3, 6, 3, 6, 6, 6, 6], distances, weights)

print(delta)
print(a//1000)
print(b//1000)
