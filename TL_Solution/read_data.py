import pandas as pd
import numpy as np

# def generate_data_10():
#     df = pd.read_excel('data\data10x10-54x54.xlsx', sheet_name='10x10', usecols='S:AB')
#     flow_10 = df.iloc[4:14]
    
#     df = pd.read_excel('data\data10x10-54x54.xlsx', sheet_name='10x10', usecols='E:N')
#     coords = df.iloc[1:3].to_numpy()

#     nodes = 10
#     hubs = 5
#     ksi, delta, alpha, beta = 3, 2, 0.4, 0.5
    
#     return nodes, coords.T, flow_10, hubs, ksi, delta, alpha, beta

# nodes, coords, flows, hubs, ksi, delta, alpha, beta = generate_data_10()

# def save_data_to_txt_10(filename, nodes, coords, flows, hubs, ksi, delta, alpha, beta):
#     flows_array = flows.to_numpy()
    
#     with open(filename, 'w') as f:
#         f.write(f"{nodes}\n")
#         for coord in coords:
#             f.write(f"{coord[0]} {coord[1]}\n")
#         for row in flows_array:
#             f.write(" ".join(map(str, row)) + "\n")
#         f.write(f"{hubs}\n")
#         f.write(f"{delta:.6f}\n")
#         f.write(f"{alpha:.6f}\n")
#         f.write(f"{ksi:.6f}\n")
#         f.write(f"{beta:.6f}\n")
#         print("Complete")
        
# save_data_to_txt_10(f'data/{nodes}.{hubs}', nodes, coords, flows, hubs, ksi, delta, alpha, beta)


def generate_data_54():
    df = pd.read_excel('data\data10x10-54x54.xlsx', sheet_name='flow', usecols='D:BE')
    flow_54 = df.iloc[3:57]
    
    df = pd.read_excel('data\data10x10-54x54.xlsx', sheet_name='dist', usecols='E:BF')
    coords = df.iloc[0:2].to_numpy()

    df = pd.read_excel('data\data10x10-54x54.xlsx', sheet_name='flow', usecols='BI')
    capacity = df.iloc[3:57].to_numpy()

    print(capacity)
    
    nodes = 54
    hubs = 4
    ksi, delta, alpha, beta = 3, 2, 0.4, 0.5
    
    return nodes, coords.T, flow_54, hubs, ksi, delta, alpha, beta, capacity
    
nodes, coords, flows, hubs, ksi, delta, alpha, beta, capacity = generate_data_54()

    
def save_data_to_txt_54(filename, nodes, coords, flows, hubs, ksi, delta, alpha, beta, capacity):
    flows_array = flows.to_numpy()
    
    with open(filename, 'w') as f:
        f.write(f"{nodes}\n")
        for coord in coords:
            f.write(f"{coord[0]} {coord[1]}\n")
        for row in flows_array:
            f.write(" ".join(map(str, row)) + "\n")
        f.write(f"{hubs}\n")
        f.write(f"{delta:.2f}\n")
        f.write(f"{alpha:.2f}\n")
        f.write(f"{ksi:.2f}\n")
        f.write(f"{beta:.2f}\n")
        for cap in capacity:
            f.write(f"{cap[0]:.2f}\n")
        print("Complete")
        
save_data_to_txt_54(f'data/{nodes}.{hubs}', nodes, coords, flows, hubs, ksi, delta, alpha, beta, capacity)


