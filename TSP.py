import numpy as np
from dimod import ConstrainedQuadraticModel, Binary, Integer
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler
from itertools import chain, combinations

import time
import random
import vrplib
import csv
import os
import json
from dotenv import load_dotenv

import networkx as nx
import matplotlib.pyplot as plt



load_dotenv()

TSP_TOKEN = os.getenv('TSP_TOKEN')
dataset = os.getenv('DATASET')


colors = [ "#58FF33", "#CD6155", "#DAF7A6", "#FFC300", "#A569BD", "#5499C7", "#45B39D", "#6E2C00", "#FF33D1", "#FFFFFF", "#000000", "#33FFAF", "#33FFE0", "#FF3333"]

csv_filename = "./csv_files/tsp_input.csv"
with open(csv_filename) as f:
    reader = csv.reader(f)
    centroid_paths = list(line for line in reader)
node_list = [list(map(int, lst)) for lst in centroid_paths]
instance_size = os.getenv('INST_SIZE')
instance = vrplib.read_instance(f"./data_instances/{instance_size}.vrp")
solution = vrplib.read_solution(f"./solution_instances/{instance_size}.sol")

def TSP(node_list):
    instance_size = os.getenv('INST_SIZE')
    instance = vrplib.read_instance(f"./data_instances/{instance_size}.vrp")
    solution = vrplib.read_solution(f"./solution_instances/{instance_size}.sol")
    n=len(node_list)
    # strp=instance.name.partition("k")[2]
    p=1#Number of trucks
    distances=instance.get('edge_weight').tolist()

    node_list = np.array(node_list)

    # Helper functions

    # Generate all subsets of nodes with cardinality >= 2
    # def powerset(iterable):
    #     '''powerset([1,2,3]) --> [(1,2) (1,3) (2,3) (1,2,3)]'''
    #     s = list(iterable)
        
    #     # Create all combinations from s, each combination object containing sets of increasing size
    #     combination_list = [combinations(s, r) for r in range(2, len(s))]
        
    #     # Chain them together and return single list of desired subsets
    #     return list(combination_list)

    # p_t_2_plus = powerset(node_list)

    c=np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            c[i][j]=distances[node_list[i]][node_list[j]]
            
    # V=int(n*(n-1)*p)
    # D=instance.demands
    # Q=instance.capacity

    x = np.array([[[Binary(f'x_{r}_{i}_{j}') for j in range(n)] for i in range(n)] for r in range(p)])

    cqm = ConstrainedQuadraticModel()

    cqm.set_objective(quicksum(c[i][j]*x[r][i][j] for r in range(p) for i in range(n) for j in range(n) if(j!=i)))

    # Each node is visited only once
    for j in range(1,n):
        cqm.add_constraint(quicksum(x[r][i][j] for r in range(p) for i in range(n) if i!=j)==1, label=f'Constraint1_{j}')

    # Each vehicle must leave the depot
    for r in range(p):
        cqm.add_constraint(quicksum(x[r][0][j] for j in range(1,n))==1, label=f'Constraint2_{r}')

    # The order of the route is valid and maintained

    for j in range(n):
        for r in range(p):
            cqm.add_constraint(quicksum(x[r][i][j] for i in range(n) if i!=j)-quicksum(x[r][j][i] for i in range(n) if i!=j)==0,label=f'Constraint3_{j}_{r}')

    B = n

    s_max = n

    s =[[None]*(p) for _ in range(n)]

    for i in range(n):
        for r in range(p):
            s[i][r] = Integer(lower_bound=1,upper_bound = s_max,label=f't.{i}.{r}')

    for i in range(1,n):
        for j in range(1,n):
            if i!=j:
                for r in range(p):
                    cqm.add_constraint((s[j][r]-(s[i][r]+1)+B*(1-x[r][i][j]))>=0)

    # Each vehicle does not exceed its capacity
    # for r in range(p):
    #     cqm.add_constraint(quicksum(D[j]*x[r][i][j] for i in range(n) for j in range(1,n) if j!=i)<=Q,label=f'Constraint4_{r}')

    # # Sub-tours are prevented from being included in the solution
    # def constraint_5(X, subset):
    #     sum = 0
            
    #     for r in range(p):
    #         for i in subset:
    #             for j in subset:
    #                 if i != j:
    #                     sum += X[r][i][j] 

    #     return sum

    # for s in p_t_2_plus:
    #     for subset in s:
    #         cqm.add_constraint(constraint_5(X=x, subset = subset) \
    #                            <= len(subset) - 1)



    # print(t)

    def get_token():
        return TSP_TOKEN



    print("Starting D wave")
    startime=time.time()
    sampler=LeapHybridCQMSampler(token=get_token())
    sampleset = sampler.sample_cqm(cqm,time_limit=150,label='CVRP')
    feasible_sampleset=sampleset.filter(lambda row:row.is_feasible)
    end_time=time.time()
    try:
        best_solution=feasible_sampleset.first.sample
    except:
        print("No feasible solution found")
        exit()

    print("\n Total execution time for "+str(n)+" nodes "+str(p)+" vehicles "+"takes : "+str(end_time-startime)+"seconds\n")

    truck_stops=[]
    routes=[[] for _ in range(p)]
    for key,val in best_solution.items():
        if val==1.0:
            if "x_" in key:
                truck_stops.append(key.split('_')[1:])
                routes[int(truck_stops[-1][0])].append(truck_stops[-1][1:])

    paths = []

    total_cost=0

    for_graph = []

    for i in range(p):
        current_route=routes[i]
        current_cost=0
        temp = []
        for r in current_route:
            current_cost+=c[int(r[0])][int(r[1])]
        print("\nTruck",i,"route:")
        for r in current_route:
            #print(r)
            t=[]
            t.append(node_list[int(r[0])]) 
            t.append(node_list[int(r[1])])
            print(t)
            for_graph.append(t)
            temp.append(tuple(r))
        print("\nTruck",i,"cost:",current_cost)
        total_cost+=current_cost
        paths.append(temp)

    print("\nTotal cost:\t",total_cost)

    print("\nClassical Solution Route\t",solution.get("routes"))
    print("\nClassical Solution Total cost:\t",solution.get("cost"))
    return (total_cost,for_graph)

paths = []
total_cost = 0

for i in range(len(node_list)):
    solution = TSP(node_list[i])
    total_cost+= solution[0]
    paths.append(solution[1])

print('\n\nTotal Quantum Cost = ',total_cost)

print("\n\n")

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
plt.savefig("graph", bbox_inches=None)


# # for l in range(len(paths)):
# #     k = G.subgraph(get_sub_nodes(paths[l]))
# #     nx.draw_networkx(k, pos, with_labels=True, edge_color=colors[l], node_color=colors[l])
# plt.savefig("final", bbox_inches=None)