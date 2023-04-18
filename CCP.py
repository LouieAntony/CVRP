import json
import os

import numpy as np
import math
import matplotlib.pyplot as plt
import cvrplib

import skfuzzy as fuzz
from dotenv import load_dotenv

load_dotenv()

dataset = os.getenv('DATASET')

instance, solution = cvrplib.download(dataset,solution=True)
distances = [distance for distance in instance.distances]
trucks = instance.name.partition("k")[2]

# Set the maximum sum of cluster points
capacity = instance.capacity
coords_original = [coordinates for coordinates in instance.coordinates]
depot = instance.coordinates[0]
demands = [demand for demand in instance.demands]

# Define the number of clusters
k = int(trucks)

# ******** ccp goes in here ********
WSS = []
n_clusters = 0
n_clusters_list = list(range(k, 2 * k + 1))
n_clusters_list
for i in range(len(n_clusters_list)):
  n_clusters = n_clusters_list[i]
  # print(n_clusters)
  coords = list(coords_original)

  for c in range(n_clusters - 1):
    coords.insert(0, depot)

  coords = np.array(coords)

  # print(coords.shape)
  # Apply fuzzy c-means clustering
  cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
      coords.T, n_clusters, 2, error=0.005, maxiter=1000, init=None
  )
  
  # Predict cluster membership for each data point
  cluster_membership = np.argmax(u, axis=0)
  
  # Print the cluster centers
  # print('Cluster Centers:', cntr)
  
  # Print the cluster membership for each data point
  # print('Cluster Membership:', cluster_membership)

  WSS.append(0)

  for node in range(len(cluster_membership)):
    dist = math.dist(coords[node], cntr[cluster_membership[node]])
    WSS[i] += dist
# plt.scatter(n_clusters_list, WSS)
# Remove all instances of depot
u_depot = np.array(u[ : , n_clusters : ])
# Node preferences
preferences = []

# Cluster assignment
cluster_assignment = {}

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
  cluster_with_highest_preference[0]
  sorted_cluster_with_highest_preference = []

  for row in cluster_with_highest_preference:
    sorted_cluster_with_highest_preference.append(sorted(row, key = lambda i: i[1], reverse = True))
  sorted_cluster_with_highest_preference[0]
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
        assigned_nodes.append(node)

  nodes = [node for node, _ in preferences]

  new_preferences = [preference for preference in preferences if preference[0] not in assigned_nodes]
  preferences = new_preferences
  len(new_preferences)
  sum = 0


  if len(new_preferences)!=0:
      node_assign(preferences)
  sum = 0


  for cluster in cluster_assignment.items():
    cluster_info = cluster[1]
    nodes = cluster_info['nodes']

    centroid = [0.0, 0.0]

    if len(nodes) == 0:
      continue

    for node in nodes:
      centroid[0] += coords_original[node][0]
      centroid[1] += coords_original[node][1]

    centroid[0] = centroid[0] / len(nodes)
    centroid[1] = centroid[0] / len(nodes)

    cluster_info['centroid'] = centroid
    cluster_info['demand'] = 100 - cluster_info['capacity']
    del cluster_info['capacity']

    sum = sum + len(cluster[1]['nodes'])
    # print(cluster)

  return cluster_assignment

# **********************************

output = node_assign(preferences)

keys = []

for c in output.items():
    if not c[1].get("centroid"):
        keys.append(c[0])
for k in keys:
    del output[k]

ccp_output = {}

i = 0
for op in output.values():
    ccp_output[i] = op
    i+=1

out_file = open("./csv_files/ccp_output.csv", "w")

json.dump(ccp_output, out_file, indent = 3)
  
out_file.close()