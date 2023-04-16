import json
import csv

ccp_output = open("./csv_files/ccp_output.csv",)

input = json.load(ccp_output)

# print(input)


csv_filename = "./csv_files/cluster_centroid_map.csv"
with open(csv_filename) as f:
    reader = csv.reader(f)
    centroid_paths = list(line for line in reader)
print(centroid_paths)

cluster_nodes = []
for path in centroid_paths:
    temp = [0]
    path.remove('0')
    for p in path:
        temp += input[str(int(p)-1)].get("nodes")
    cluster_nodes.append(temp)

print(cluster_nodes)

with open('./csv_files/tsp_input.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for cl in cluster_nodes:
        writer.writerow(cl)