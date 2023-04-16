from CVRP import TSP 
from extend_csv import *


sample = {
    0: {'capacity': 9, 'nodes': [ 24, 27, 14, 20 ]},
    1: {'capacity': 25, 'nodes': [ 19, 31, 17, 21, 13, 7 ]},
    2: {'capacity': 1, 'nodes': [4, 11, 28, 8, 3, 2, 23 ]},
    3: {'capacity': 2, 'nodes': [10, 25, 5, 29, 15, 6,  22,9,18 ]},
    4: {'capacity': 53, 'nodes': [16, 12, 1, 30, 26]}
}

make_csv(sample)
data = read_csv('edges.csv')
total_cost=0

paths = []

for i in range(len(data)):
    solution = TSP(data[i])
    total_cost+= solution[0]
    paths.append(solution[1])

print('Total Quantum Cost =',total_cost)

file1 = open("paths.txt","w")

for p in paths:
    file1.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in p))
    file1.write("\n")
    file1.write("#################")


