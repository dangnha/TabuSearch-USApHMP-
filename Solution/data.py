from os import listdir
from os.path import isfile, join
from utils import parse_input, CalDistance

DATASET = 'AP'
INPUT_DIRECTORY = f"./data/{DATASET}/generated/"
files = [join(INPUT_DIRECTORY, f) for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]

def initial_parameter(file_db):
    file = files[files.index(f'./data/AP/generated/{file_db}')]

    n, p, alpha, delta, ksi, coords, weights = parse_input(file, DATASET)
    distances = CalDistance(coords)

    return n, p, alpha, delta, ksi, coords, weights, distances
    
def initial_coords(n, p):
    file = files[files.index(f'./data/AP/generated/{n}.{p}')]
    _, _, _, _, _, coords, _ = parse_input(file, DATASET)
    return coords

# n, p, alpha, delta, ksi, coords, weights, distances = initial_parameter("10.2")
# print(distances)

