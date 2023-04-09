import numpy as np
from dimod import ConstrainedQuadraticModel, Binary
from dimod import quicksum
from dwave.system import LeapHybridCQMSampler
from itertools import combinations

import time
import random
import cvrplib

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

# y = {}
# for i in range(n):
#     for k in range(m):
#         y[i, k] = model.addVar(vtype=gp.GRB.BINARY, name=f'y_{i}_{k}')
y=[[Binary(f'y_{i}_{k}') for k in range(p)] for i in range(n)]
#print(y)
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

for r in range(p):
    for i in range(n):
        cqm.add_constraint(quicksum(x[i][j][r] for j in range(n) if j != i) == y[i][r])
        cqm.add_constraint(quicksum(x[j][i][r] for j in range(n) if j != i) == y[i][r])
    for S in combinations(range(n), r+1):
        cqm.add_constraint(quicksum(x[i][j][r] for i in S for j in S if i != j) <= len(S)-1)

# for k in range(p):
#     for i in range(n):
#         cqm.add_constraint(sum(x[i][j][k] for j in range(n) if j != i) == y[i][k])
#         cqm.add_constraint(sum(x[j][i][k] for j in range(n) if j != i) == y[i][k])
#     for S in combinations(range(n), k+1):
#         cqm.add_constraint(sum(x[i][j][k] for i in S for j in S if i != j) <= len(S)-1)

def get_token():
    return 'DEV-1d60aad88f8696c54de9bda08d32edd98f3b7130'

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
