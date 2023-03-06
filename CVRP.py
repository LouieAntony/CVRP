import numpy as np
from dimod import ConstrainedQuadraticModel, Binary
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler

import time

#from shapely.geometry import Point
import random
import cvrplib

import networkx as nx
import matplotlib.pyplot as plt


def edge_gen(list):
    edge_list = []
    for i in range(len(list)-1):
        edge_list.append((list[i],list[i+1]))
    edge_list.append((list[-1],'0'))
    return edge_list

colors = [ "#58FF33", "#CD6155", "#DAF7A6", "#FFC300", "#A569BD", "#5499C7", "#45B39D", "#6E2C00", "#FF33D1", "#FFFFFF", "#000000", "#33FFAF", "#33FFE0", "#FF3333"]

instance, solution = cvrplib.download('A-n32-k5',solution=True)
n=instance.dimension
strp=instance.name.partition("k")[2]
p=int(strp)#Number of trucks

distances=instance.distances

c=np.zeros((n,n))
for i in range(0,n):
    for j in range(0,n):
        c[i][j]=distances[i][j]
        
V=int(n*(n-1)*p)
D=instance.demands
Q=instance.capacity

x=[[[Binary(f'x_{r}_{i}_{j}') for j in range(n)] for i in range(n)] for r in range(p)]

cqm= ConstrainedQuadraticModel()

cqm.set_objective(quicksum(c[i][j]*x[r][i][j] for r in range(p) for i in range(n) for j in range(n) if(j!=i)))

for j in range(1,n):
    cqm.add_constraint(quicksum(x[r][i][j] for r in range(p) for i in range(n) if i!=j)==1, label=f'Eq2_{j}')

for r in range(p):
    cqm.add_constraint(quicksum(x[r][0][j] for j in range(1,n))==1, label=f'Eqn3_{r}')

for j in range(n):
    for r in range(p):
        cqm.add_constraint(quicksum(x[r][i][j] for i in range(n) if i!=j)-quicksum(x[r][j][i] for i in range(n) if i!=j)==0,label=f'Eq4_{j}_{r}')

for r in range(p):
    cqm.add_constraint(quicksum(D[j]*x[r][i][j] for i in range(n) for j in range(1,n) if j!=i)<=Q,label=f'Eqn5_{r}')

import dimod
B=2*n

T_max=max(2*n-p+1,1)

t=[[None]*(p) for _ in range(n)]

for i in range(n):
    for r in range(p):
        t[i][r]=dimod.Integer(lower_bound=1,upper_bound=T_max,label=f't.{i}.{r}')

for i in range(1,n):
    for j in range(1,n):
        if i!=j:
            for k in range(p):
                cqm.add_constraint((t[j][k]-(t[i][k]+1)+B*(1-x[k][i][j]))>=0)

def get_token():
    return 'DEV-84bd4a159c19999c61d45bf77755d8a37754ba12'


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
for i in range(p):
    current_route=routes[i]
    current_cost=0
    temp = []
    for r in current_route:
        current_cost+=c[int(r[0])][int(r[1])]
    print("\nTruck",i,"route:")
    for r in current_route:
        print(r)
        temp.append(r[0])
    print("\nTruck",i,"cost:",current_cost)
    total_cost+=current_cost
    paths.append(temp)

G = nx.Graph()
for i in range(len(instance.coordinates)):
    G.add_node(str(i),pos=tuple(instance.coordinates[i]))
for l in paths:
    G.add_edges_from(edge_gen(l))

nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=10)

for l in range(len(paths)):
    k = G.subgraph(paths[l])
    nx.draw_networkx(k, nx.get_node_attributes(G, 'pos'), with_labels=True, edge_color=colors[l], node_color=colors[l])
plt.savefig("solution", bbox_inches=None)

print("\nTotal cost:\t",total_cost)

print("\nClassical Solution Route\t",solution.routes)
print("\nClassical Solution Total cost:\t",solution.cost)


#print("\n ",instance.name,"\n ")
#print("\n ",strp,"\n ")
#print(solution)