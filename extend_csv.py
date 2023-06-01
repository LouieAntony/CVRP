import csv
import pandas as pd

def prepare_tsp_input(dictionary):
    nodes = []
    for i in dictionary.values():
        n = i.get("nodes")
        n.insert(0,0)
        nodes.append((i.get("capacity"),n))
    
    return nodes

def make_csv(data):
    with open('./csv_files/edges.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        clusters = prepare_tsp_input(data)
        for cl in clusters:
            row = (cl[0], ','.join(str(x) for x in cl[1]))
            writer.writerow(row)

def read_csv(file_name):
    csv_filename = f'./csv_files/{file_name}'
    with open(csv_filename) as f:
        reader = csv.reader(f)
        lst = list(line for line in reader)

    cluster_nodes = []
    for l in lst:
        cluster_nodes.append(list(map(int, l[1].split(','))))

    return cluster_nodes