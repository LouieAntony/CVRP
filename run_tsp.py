import csv

csv_filename = './csv_files/tsp_input.csv'

with open(csv_filename) as f:
    reader = csv.reader(f)
    clusters = list(line for line in reader)

print("############")
print(clusters)
clusters = [list(map(int, lst)) for lst in clusters]

print(clusters)