#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph
from analysis import Analysis
from graph_plot import plot


# Define starting
point_list = {
    0: (1, 1),
    1: (4, 1),
    2: (1, 5),
    3: (4, 5),
    4: (2.5, 8),
    }

edge_list = {
    0: (0,1),
    1: (0,2),
    2: (0,3),
    3: (1,3),
    4: (2,3),
    5: (2,4),
    6: (3,4),
    } 

random.seed(10)
gen_size = 15

point_list, edge_list = generate_graph(n = gen_size)

G1 = Graph(pos = point_list, edge_list = edge_list)

point_guess = {
    0: (1, 1),
    1: (4, 1),
    2: (6, -5),
    3: (-3, 0),
    4: (-6, 12.1),
    } 

point_guess,_ = generate_graph(n = gen_size)

G2 = Graph(pos = point_guess, edge_list=edge_list,rigid_edge = [0])

fig,ax = plot(G1,G2)

A = Analysis(G2, n=100)
A.iterator(G1,G2)

input("Press [enter] to finish.")
