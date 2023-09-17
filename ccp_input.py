import math
import vrplib

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

def find_dist_mat(x, y):
    x1 = x[0]
    x2 = y[0]
    y1 = x[1]
    y2 = y[1]

    abscissa = (x1-x2)**2
    ordinate = (y1-y2)**2
    return math.sqrt(abscissa + ordinate)

def get_coord(data, data_instance):
    coords = data_instance.get('node_coord')
    coordinates = []
    coordinates.append(coords[0])
    for i in data.values():
        coordinates.append(i.get("centroid"))
    return coordinates

def get_demands(data):
    demands = [0]
    for i in data.values():
        demands.append(i.get('demand'))
    return demands


def ret_instance(input, data_instance):
    # original_instance, solution = cvrplib.download('A-n32-k5',solution=True)
    coordinates = get_coord(input,data_instance)
    instance = {
        "name": 'n9-k5',
        "dimension": len(input)+1,
        "n_customers": len(input),
        "depot": 0,
        "customers": [i for i in range(1,len(input)+1)],
        "capacity": data_instance.get('capacity'),
        "distances": [[find_dist_mat(x,y) for x in coordinates] for y in coordinates],
        "demands": get_demands(input),
        "coordinates": coordinates, 
        "distance_limit": math.inf,
        "service_times": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }

    return objectview(instance)