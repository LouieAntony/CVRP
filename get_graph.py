import cvrplib
import numpy as np
from dimod import ConstrainedQuadraticModel, Binary, Integer
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler
from itertools import chain, combinations

import time
import random
import cvrplib

import networkx as nx
import matplotlib.pyplot as plt

instance, solution = cvrplib.download('A-n32-k5',solution=True)

paths = [
    [ #6
        (0, 14),
        (24, 27),
        (27, 20),
        (14, 24),
        (20, 0)
    ], 
    [ #9
        (0, 7),
        (19, 31),
        (31, 21),
        (17, 19),
        (21, 0),
        (13, 17),
        (7, 13)
    ], 
    [ #8
        (0, 8),
        (4, 28),
        (11, 4),
        (28, 23),
        (8, 11),
        (3, 2),
        (2, 0),
        (23, 3)
    ], 
    [ #8
        (0, 5),
        (10, 15),
        (25, 10),
        (5, 25),
        (29, 22),
        (15, 29),
        (6, 0),
        (22, 9),
        (9, 18),
        (18, 6)
    ],
    [
        (0, 12),
        (16, 26),
        (12, 1),
        (1, 16),
        (30, 0),
        (26, 30)
    ]
    # , 
    # [ #9
    #     (0, 5),
    #     (14, 29),
    #     (17, 28),
    #     (29, 1),
    #     (28, 14),
    #     (1, 0),
    #     (5, 15),
    #     (10, 17),
    #     (15, 10)
    # ]
    # ,
    # [ #8
    #     (0, 4),
    #     (27, 19),
    #     (38, 27),
    #     (19, 26),
    #     (39, 38),
    #     (26, 23),
    #     (4, 39),
    #     (23, 0)
    # ]
]

colors = [ "#58FF33", "#CD6155", "#DAF7A6", "#FFC300", "#A569BD", "#5499C7", "#45B39D", "#6E2C00", "#FF33D1", "#FFFFFF", "#000000", "#33FFAF", "#33FFE0", "#FF3333"]

def get_sub_nodes(lis):
    i = lis[0]
    for t in lis[1:]:
        i+=t
    return list(i)


G = nx.Graph()
for i in range(len(instance.coordinates)):
    G.add_node(i,pos=tuple(instance.coordinates[i]))
for l in paths:
    G.add_edges_from(l)

nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=10)

for l in range(len(paths)):
    k = G.subgraph(get_sub_nodes(paths[l]))
    nx.draw_networkx(k, nx.get_node_attributes(G, 'pos'), with_labels=True, edge_color=colors[l], node_color=colors[l])
plt.savefig("finall", bbox_inches=None)


# # for l in range(len(paths)):
# #     k = G.subgraph(get_sub_nodes(paths[l]))
# #     nx.draw_networkx(k, pos, with_labels=True, edge_color=colors[l], node_color=colors[l])
# plt.savefig("final", bbox_inches=None)