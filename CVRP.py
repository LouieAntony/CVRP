import numpy as np
from dimod import ConstrainedQuadraticModel, Binary
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler
from itertools import chain, combinations

import time
import random
import cvrplib

instance, solution = cvrplib.download('A-n32-k5',solution=True)
n=instance.dimension
strp=instance.name.partition("k")[2]
p=int(strp)#Number of trucks
distances=instance.distances

node_list = list(range(1, n))

# Helper functions

# Generate all subsets of nodes with cardinality >= 2
def powerset(iterable):
    '''powerset([1,2,3]) --> [(1,2) (1,3) (2,3) (1,2,3)]'''
    s = list(iterable)
    
    # Create all combinations from s, each combination object containing sets of increasing size
    combination_list = [combinations(s, r) for r in range(2, len(s))]
    
    # Chain them together and return single list of desired subsets
    return list(combination_list)

p_t_2_plus = powerset(node_list)

c=np.zeros((n,n))
for i in range(0,n):
    for j in range(0,n):
        c[i][j]=distances[i][j]
        
V=int(n*(n-1)*p)
D=instance.demands
Q=instance.capacity

x=[[[Binary(f'x_{r}_{i}_{j}') for j in range(n)] for i in range(n)] for r in range(p)]

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

# Each vehicle does not exceed its capacity
for r in range(p):
    cqm.add_constraint(quicksum(D[j]*x[r][i][j] for i in range(n) for j in range(1,n) if j!=i)<=Q,label=f'Constraint4_{r}')

# Sub-tours are prevented from being included in the solution
for s in p_t_2_plus:
    for subset in s:
        cqm.add_constraint(quicksum( \
                                x[r][i][j] \
                                for j in subset \
                                for i in subset \
                                if i != j \
                                for k in range(p) \
                            ) <= len(subset) - 1)

def get_token():
    return 'DEV-78aeea4bb135991b8b476e1a4a09307a3d458858'


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

total_cost=0
for i in range(p):
    current_route=routes[i]
    current_cost=0
    for r in current_route:
        current_cost+=c[int(r[0])][int(r[1])]
    print("\nTruck",i,"route:")
    for r in current_route:
        print(r)
    print("\nTruck",i,"cost:",current_cost)
    total_cost+=current_cost

print("\nTotal cost:\t",total_cost)

print("\nClassical Solution Route\t",solution.routes)
print("\nClassical Solution Total cost:\t",solution.cost)