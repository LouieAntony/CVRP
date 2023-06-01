import numpy as np
import matplotlib.pyplot as plt
import vrplib
import os
import skfuzzy as fuzz
import shutil
from scipy.spatial import distance_matrix
from dotenv import load_dotenv

load_dotenv()

from extend_csv import *

instance_size = os.getenv('INST_SIZE')

os.mkdir('./data_instances')
os.mkdir('./solution_instances')

vrplib.download_instance(f'{instance_size}','./data_instances')
vrplib.download_solution(f'{instance_size}','./solution_instances')
instance = vrplib.read_instance(f"./data_instances/{instance_size}.vrp")
solution = vrplib.read_solution(f"./solution_instances/{instance_size}.sol")
trucks = instance.get('name').partition("k")[2]

# Set the maximum sum of cluster points
capacity = instance.get('capacity')
coords_original = [coordinates for coordinates in instance.get('node_coord')]
depot = instance.get('node_coord')[0]
demands = instance.get('demand').tolist()
distances = instance.get('edge_weight').tolist()

# Define the number of clusters
n_clusters = int(trucks)
for i in range(n_clusters - 1):
  coords_original.insert(0, depot)

coords = np.array(coords_original)
def demand_constraint(labels, coords, demands, capacity):
    for i in np.unique(labels):
        if np.sum(demands[i]) > capacity:
            return False
    return True

cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    coords.T, n_clusters, 2, error=0.005, maxiter=1000, init=None
)
 
# Predict cluster membership for each data point
cluster_membership = np.argmax(u, axis=0)
 
# Print the cluster centers
print('Cluster Centers:', cntr)
 
# Print the cluster membership for each data point
print('Cluster Membership:', cluster_membership)

u_depot = np.array(u[ : , n_clusters : ])

preferences = []

# Cluster assignment
cluster_assignment = {}
node_assignment = [None] * u_depot.shape[1]

for cluster in range(n_clusters):
  cluster_assignment[cluster] = {}
  cluster_assignment[cluster]['capacity'] = capacity
  cluster_assignment[cluster]['nodes'] = []
for node in u_depot.T:
  preferences.append(list(enumerate(node)))

preferences = list(enumerate(preferences, 1))

def node_assign(preferences):
  highest_preference = []
  for node in preferences:
    h_p = max(node[1], key = lambda i : i[1])
    highest_preference.append((node[0], h_p))

    node[1].remove(h_p)
    # new_preferences.append(node)

  highest_preference[0]
  cluster_with_highest_preference = []

  for i in range(n_clusters):
    cluster_with_highest_preference.append([])

  for i in range(len(highest_preference)):
    node = highest_preference[i][0]
    h_p = highest_preference[i][1]
    cluster, preference = h_p
    cluster_with_highest_preference[cluster].append((node, preference))
  cluster_with_highest_preference
  sorted_cluster_with_highest_preference = []

  for row in cluster_with_highest_preference:
    sorted_cluster_with_highest_preference.append(sorted(row, key = lambda i: i[1], reverse = True))
  sorted_cluster_with_highest_preference[3]
  assigned_nodes = []

  for cluster in range(n_clusters):
    assignment_preference = sorted_cluster_with_highest_preference[cluster]

    for preference in assignment_preference:
      node = preference[0]
      demand = demands[node]
      capacity = cluster_assignment[cluster]['capacity']

      if cluster_assignment[cluster]['capacity'] > demand:
        cluster_assignment[cluster]['capacity'] = capacity - demand
        cluster_assignment[cluster]['nodes'].append(node)

        node_assignment[node - 1] = cluster
        assigned_nodes.append(node)

  nodes = [node for node, _ in preferences]

  new_preferences = [preference for preference in preferences if preference[0] not in assigned_nodes]
  preferences = new_preferences
  if len(new_preferences)!=0:
    node_assign(preferences)
  sum = 0

  for cluster in cluster_assignment.items():
    sum = sum + len(cluster[1]['nodes'])
    print(cluster)

  return cluster_assignment

fcm_output = node_assign(preferences)
print(fcm_output)
make_csv(fcm_output)