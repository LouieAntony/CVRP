from CVRP import TSP 
from extend_csv import *

sample = {
    0: {'capacity': 29, 'nodes': [10, 25, 29, 5, 15, 20]},
    1: {'capacity': 53, 'nodes': [3, 23, 2, 6]},
    2: {'capacity': 20, 'nodes': [21, 31, 19, 17, 13]},
    3: {'capacity': 2, 'nodes': [30, 26, 16, 24, 14, 12, 7]},
    4: {'capacity': 25, 'nodes': [8, 18, 11, 9, 22, 4, 28]}
}

# make_csv(sample)
data = read_csv('edges.csv')
total_cost=0
for i in range(len(data)):
    total_cost+=TSP(data[i])
print('Total Quantum Cost =',total_cost)

