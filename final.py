from CVRP import TSP 
from extend_csv import *
import json
import csv

data = read_csv('edges.csv')
total_cost=0

paths = []

for i in range(len(data)):
    solution = TSP(data[i])
    total_cost+= solution[0]
    paths.append(solution[1])

print('Total Quantum Cost =',total_cost)


with open('./csv_files/paths.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerows(paths)
