# Quantum Annealing for Real Time Route Optimization
In this study, we propose and compare the performance of two approaches to solve the CVRP
* Hybrid Two Step : FCM (Base clustering) + TSP (Quantum Annealing)
* Hybrid Three Step : FCM (Base clustering) + CVRP + TSP (Quantum Annealing)

This program is for the Hybrid Three Step approach (FCM (Base clustering) + CVRP + TSP (Quantum Annealing))

## What is Quantum Computing
Quantum Computing new paradigm of computing that promises near infinite parallelisation. It is a type of computing that uses quantum mechanics to perform calculations. In a quantum computer, the basic unit of information is the quantum bit, or qubit. 

## Motivation
By solving CVRP, companies can reduce their :
* Transportation costs
* Improve customer service
* Environmental benefits
* Competitive advantage
Quantum approach was used over classical approach as quantum annealing has the ability to deal with more complex problems that conventional optimization methods are unable to handle, such as those with a significant number of constraints or variables.

## Tools Used
* D-wave platform
  * D-Wave Platform is a set of software tools and services provided by D-Wave Systems.
  * The platform is designed to make easier for developers to deploy quantum computing applications.
  * The D-Wave Platform includes several components, including:
    * D-Wave Ocean software suite
    * Leap
    * Hybrid solvers

* Libraries used
  * matplotlib - Used for creating visualizations, such as charts and graphs.
  * networkx - Used for the creation, manipulation, and analysis of complex networks.
  * dimod - Used for designed and solving discrete optimization problems using QA and solvers.

* Language used
  * Python - It is known for its simplicity, readability, and ease of use.

## Installation
In Leap platform, most of the packages will come pre-installed.
The packages that need to be installed are
* python-dotenv
* vrplib
* scikit-fuzzy
* csv

## How to use?
### CCP.py
This is the clustering code. The code makes k clusters where k is twice the number of trucks. This output is stored in a csv file "ccp_output.csv" which will be saved in csv_files folder.
We have taken twice the number of trucks because when employed elbow method to find out optimal number of clusters, we have found that twice the number of clusters have provided better results comparatively.

### CVRP.py
Here the cluster centroids obtained previously (CCP.py) treated as compressed customer nodes and are clustered. The number of clusters taken here will be equal to the number of trucks so that each truck will be assiged with each of these clusters of compressed nodes. The output obtained here is stored in "cluster_centroid_map.csv".

### tsp_input.py
Here the output from CVRP.py is read and is converted to a list of nodes. That is, in each cluster, the compressed nodes are decompressed and are concatenated and then the depot node is added to it. This data is stored in "tsp_input.csv"

### TSP.py
This is file contains code for the following
* Read data stored in tsp_input.csv and feed into TSP(node_list) function.
* Function where the QUBO equations are fed into the Hybrid solver. This is where the magic happens. This code is modularised. Meaning, it is made into a function that accepts the parameter "node_list".
* Create graph by utilising networkx package. The data stored in paths.csv file is read and the final graph is created as "solution.png"

#### TSP(node_list)
This function takes a list of nodes as input and finds the optimal path for this set of nodes i.e; for each cluster.

### one.py
All the components are stitched here. That is, this file runs all the components.

### .env file
#### TSP_TOKEN
Leap hybrid solver API token for the TSP step
#### CVRP_TOKEN
Leap hybrid solver API token for the CVRP step
#### DATASET
Refers to the instance used from cvrplib

### Steps to run the program
* Step 1: Change the Hybrid Solver API tokens in the .env file with fresh ones. Everytime, the hyrbid solver time gets expired, create a new account and replace the token just in the .env file. DATASET refers to the data instance being used from the cvrplib data. When want to change the data instance and just change the DATASET in the .env file. 
* Step 2: Make sure all the packages are installed. 
* Step 3: Run the command `python one.py`

