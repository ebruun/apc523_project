#PYTHON IMPORTS
import matplotlib.pyplot as plt

#LOCAL IMPORTS
from graphs import Graph, Analysis
from graph_plot import plot


# Define starting
pos = {
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

G1 = Graph(pos = pos, edge_list = edge_list)

pos_guess = {
    0: (1, 1),
    1: (4, 1),
    2: (6, -5),
    3: (-3, 0),
    4: (-6, 12.1),
    } 

G2 = Graph(pos = pos_guess, edge_list=edge_list,rigid_edge = [0])

fig,ax = plot(G1,G2)

A = Analysis(G2, n=10)
A.iterator(G1,G2)

input("Press [enter] to finish.")
