import csv
import pandas as pd

def prepare_tsp_input(dictionary):
    nodes = {}
    for i in dictionary.values():
        n = i.get("nodes")
        n.insert(0,0)
        nodes[i.get("capacity")] = n
    
    return nodes

def make_csv(data):
    with open('edges.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        clusters = prepare_tsp_input(data)
        for key, value in clusters.items():
            row = (key, ','.join(str(x) for x in value))
            writer.writerow(row)

def read_csv(file_name):
    csv_filename = file_name
    with open(csv_filename) as f:
        reader = csv.reader(f)
        lst = list(line for line in reader)

    cluster_nodes = []
    for l in lst:
        cluster_nodes.append(list(map(int, l[1].split(','))))

    return cluster_nodes