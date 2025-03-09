import numpy as np
def calculate_correlation_coefficient(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    correlation_coefficient = np.corrcoef(X, Y)[0, 1]
    return float(round(correlation_coefficient, 2))

X = [1, 1, 1, 1, 1]
Y = [1, 1, 1, 1, 1]

calculate_correlation_coefficient(X, Y)