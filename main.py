#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph
from analysis import Analysis
from graph_plot import plot, plot_iterations, plot_animations

from inputs.input_structure import p1, e1 #pre-defined structures
from inputs.input_init_conditions import ic1, ic2 #pre-defined structures


##########################################################
# 1. Create target structure
##########################################################
random.seed(10)
gen_size = 20

vertices = p1
edges = e1
#vertices, edges = generate_graph(n = gen_size, fac = 1)

G1 = Graph(vertex_list = vertices, edge_list = edges)


##########################################################
# 2. Set initial conditions
##########################################################
vertices_guess = ic1
#vertices_guess ,_ = generate_graph(n = gen_size, fac = 5)

G2 = Graph(vertex_list = vertices_guess, edge_list = edges, rigid_edge = [0])

fig,ax = plot(G1,G2)


##########################################################
# 3. Perform Newton-Raphson analysis
##########################################################
A = Analysis(G2, max_iter=100, btrack = False)
A.iterator(G1,G2)


##########################################################
# 4. Output
##########################################################
#plot_iterations(G1, A.saved_iterations)
plot_animations(G1, A.saved_iterations, 'outputs/without_backtrack.gif')

input("Press [enter] to finish.")

#CODE TO ANALYZE PRODUCED STRUCTURE