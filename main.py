#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph, generate_graph_guess
from analysis import Analysis
from graph_plot import Plotter

from inputs.input_structure import p1, e1, p2, e2, p3, e3 #pre-defined structures
from inputs.input_init_conditions import ic1_1, ic1_2, ic2_1, ic3_1 #pre-defined structures


##########################################################
# 1. Create target structure
##########################################################
random.seed(12)
gen_size = 20

# vertices, edges = generate_graph(n = gen_size, fac = 1)

# vertices = p2
# edges = e2
# edge_lens = [2.0, 2.0, 7/4, 2.0, 197/100, 27/10, 11/5, 29/10, 43/20]

# G1 = Graph(vertex_list = vertices, edge_list = edges, edge_lengths=edge_lens)

vertices = p3
edges = e3

G1 = Graph(vertex_list = vertices, edge_list = edges)


##########################################################
# 2. Set initial conditions
##########################################################
vertices_guess = ic3_1
#vertices_guess = generate_graph_guess(n = gen_size, vertex_list = vertices, fac = 5)

G2 = Graph(vertex_list = vertices_guess, edge_list = edges, rigid_edge = [0])

P = Plotter(G1)
P.plot_initial(G2)


##########################################################
# 3. Perform Newton-Raphson analysis
##########################################################
A = Analysis(btrack = "peterson", max_iter=100, gradient_steps = 0)
A.iterator(G1,G2, P)

P.error_plot(A.saved_iterations)


##########################################################
# 4. Output
##########################################################
#plot_iterations(G1, A.saved_iterations)
#P.plot_animations(A.saved_iterations,'outputs/simple.gif')

input("Press [enter] to finish.")

#CODE TO ANALYZE PRODUCED STRUCTURE
