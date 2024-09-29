from os import listdir
from os.path import isfile, join
from utils import parse_input, CalDistance

DATASET = 'AP'
INPUT_DIRECTORY = f"./data/"
files = [join(INPUT_DIRECTORY, f) for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]
print(files)

def initial_parameter(file_db):
    file = files[files.index(f'./data/{file_db}')]

    n, p, alpha, delta, ksi, coords, weights, beta, capacity_array = parse_input(file, DATASET)
    distances = CalDistance(coords)

    return n, p, alpha, delta, ksi, coords, weights, distances, beta, capacity_array
    
    
# n, p, alpha, delta, ksi, coords, weights, distances, beta, capacity_array = initial_parameter("54.3")
# print(distances.shape)
    
def initial_coords(n, p):
    file = files[files.index(f'./data/{n}.{p}')]
    _, _, _, _, _, coords, _, _, _ = parse_input(file, DATASET)
    return coords

# _, _, _, _, _, _, _, distances, _ = initial_parameter("54.3")
# print(distances[0][1])

