import numpy as np
from dimod import ConstrainedQuadraticModel, Binary, Integer
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler
from itertools import chain, combinations

import time
import random
import vrplib

import networkx as nx
import matplotlib.pyplot as plt

import os
from dotenv import load_dotenv
import json
import csv

load_dotenv()

instance_size = os.getenv('INST_SIZE')

vrplib.download_instance(f'{instance_size}','./data_instances')

instance = vrplib.read_instance(f"./data_instances/{instance_size}.vrp")

readback = []
with open('./csv_files/paths.csv', 'r') as readed:
    reader = csv.reader(readed)
    readback = list(reader)

paths = []

for i in readback:
    path = []
    for j in i:
        path.append(eval(j))
    paths.append(path)
    
colors = [ "#58FF33", "#CD6155", "#DAF7A6", "#FFC300", "#A569BD", "#5499C7", "#45B39D", "#6E2C00", "#FF33D1", "#FFFFFF", "#000000", "#33FFAF", "#33FFE0", "#FF3333"]

def get_sub_nodes(lis):
    i = lis[0]
    for t in lis[1:]:
        i+=t
    return list(i)

coords = [coordinates for coordinates in instance.get('node_coord')]

G = nx.Graph()
for i in range(len(coords)):
    G.add_node(i,pos=tuple(coords[i]))
for l in paths:
    G.add_edges_from(l)

nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=10)

for l in range(len(paths)):
    k = G.subgraph(get_sub_nodes(paths[l]))
    nx.draw_networkx(k, nx.get_node_attributes(G, 'pos'), with_labels=True, edge_color=colors[l], node_color=colors[l])
plt.savefig("solution", bbox_inches=None)


# # for l in range(len(paths)):
# #     k = G.subgraph(get_sub_nodes(paths[l]))
# #     nx.draw_networkx(k, pos, with_labels=True, edge_color=colors[l], node_color=colors[l])
# plt.savefig("final", bbox_inches=None)