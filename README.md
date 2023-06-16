# Quantum Annealing for Real Time Route Optimization
In this study, we propose and compare the performance of two approaches to solve the CVRP
* Hybrid Two Step : FCM (Base clustering) + TSP (Quantum Annealing)
* Hybrid Three Step : FCM (Base clustering) + CVRP + TSP (Quantum Annealing)

This program is about the Hybrid Two Step approach (FCM (Base clustering) + TSP (Quantum Annealing))

## What is Quantum COmputing
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
  * dimod - Used for designed and solving discrete optimization problems using QA and solvers. ​

* Language used
  * Python - It is known for its simplicity, readability, and ease of use.​

## Installation
In Leap platform, most of the packages will come pre-installed.
The packages that need to be installed are
* python-dotenv
* vrplib
* scikit-fuzzy
* csv

## How to use?
### extend_csv.py 
This file contains the code for storing and readint data in csv files.
#### prepare_tsp_input(dictionary):
This function adds the depot node to the lists of nodes of each cluster.
#### make_csv(data):
Stores the data obtained as output from fcm in a csv file with the name "edges.csv"
#### read_csv(file_name):
Reads the data stored in the file passed as a parameter.

### fcm.py 
This is the clustering code. The code makes n clusters where n is the number of trucks. This output is stored in a csv file "edges.csv" which will be saved in csv_files folder. 

### CVRP.py
This is the file with the code where the QUBO equations are fed into the Hybrid solver. This is where the magic happens. This code is modularised. Meaning, it is made into a function that accepts the parameter "node_list".
#### TSP(node_list)
This function takes a list of nodes as input and finds the optimal path for this set of nodes i.e; for each cluster.

### final.py
Here, the edges.csv file is read, the data that was obtained as output from fcm.py is taken and each cluster is fed into the TSP fucntion from CVRP.py. The output of TSP function is stored in paths.csv file which is used for preparing graph.

### get_graph.py
This file contains the code to create graph by utilising networkx package. The data stored in paths.csv file is read and the final graph is created as "solution.png"

### one.py
All the components are stitched here. That is, this file runs all the components.

### Steps to run the program
* Step 1: Change the Hybrid Solver API token in the .env file with a fresh one. Everytime, the hyrbid solver time gets expired, create a new account and replace the token just in the .env file. INST_SIZE refers to the data instance being used from the cvrplib data. When want to change the data instance and just change the INST_SIZE in the .env file. 
* Step 2: Make sure all the packages are installed. 
* Step 3: Run the command `python one.py`

