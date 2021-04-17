#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph
from analysis import Analysis
from graph_plot import plot, plot_iterations, plot_animations


# Define starting
point_list = {
    0: (1, 1),
    1: (4, 1),
    2: (1, 5),
    3: (4, 5),
    4: (2.5, 8),
    5: (4, 7),
    6: (7.5, 3),
    7: (7, 9),
    8: (4.5, 9),
    9: (9, 3),
    }

edge_list = {
    0: (0,1),
    1: (0,2),
    2: (0,3),
    3: (1,3),
    4: (2,3),
    5: (2,4),
    6: (3,4),
    7: (5,4),
    8: (5,3),
    9: (6,5),
    10: (6,1),
    11: (7,5),
    12: (7,6),
    13: (8,4),
    14: (8,7),
    15: (9,7),
    16: (9,6),
    } 

random.seed(10)
gen_size = 20

#point_list, edge_list = generate_graph(n = gen_size)

G1 = Graph(pos = point_list, edge_list = edge_list)

point_guess = {
    0: (1, 1),
    1: (4, 1),
    2: (6, -5),
    3: (-3, 0),
    4: (-6, 12.1),
    5: (6, 8),
    6: (8,1),
    7: (10,10),
    8: (0,10),
    9: (10,1.5),
    } 

# point_guess = {
#     0: (1, 1),
#     1: (4, 1),
#     2: (-6, -1),
#     3: (3, 2),
#     4: (6, -5),
#     5: (2, -4),
#     6: (1,1),
#     7: (5,2),
#     8: (-2,5),
#     9: (1,2.1),
#     } 

#point_guess,_ = generate_graph(n = gen_size)

G2 = Graph(pos = point_guess, edge_list=edge_list,rigid_edge = [0])

fig,ax = plot(G1,G2)

A = Analysis(G2, n=100)
A.iterator(G1,G2)


#plot_iterations(G1, A.saved_iterations)
plot_animations(G1, A.saved_iterations)


input("Press [enter] to finish.")
