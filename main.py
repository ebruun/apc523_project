#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph, generate_graph_guess
from analysis import Analysis
from graph_plot import plot, plot_iterations, plot_animations

from inputs.input_structure import p1, e1, p2, e2 #pre-defined structures
from inputs.input_init_conditions import ic1_1, ic1_1, ic2_1 #pre-defined structures


##########################################################
# 1. Create target structure
##########################################################
random.seed(12)
gen_size = 6

#vertices, edges = generate_graph(n = gen_size, fac = 1)

# vertices = p2
# edges = e2
# edge_lens = [2.0, 2.0, 7/4, 2.0, 197/100, 27/10, 11/5, 29/10, 43/20]

# G1 = Graph(vertex_list = vertices, edge_list = edges, edge_lengths=edge_lens)

vertices = p1
edges = e1

G1 = Graph(vertex_list = vertices, edge_list = edges)

##########################################################
# 2. Set initial conditions
##########################################################
vertices_guess = ic1_1
#vertices_guess = generate_graph_guess(n = gen_size, vertex_list = vertices, fac = 5)

G2 = Graph(vertex_list = vertices_guess, edge_list = edges, rigid_edge = [0])

fig,ax = plot(G1,G2)


##########################################################
# 3. Perform Newton-Raphson analysis
##########################################################

A = Analysis(G2, max_iter=200, btrack = "peterson", gradient_steps = 60)
A.iterator(G1,G2)


##########################################################
# 4. Output
##########################################################
#plot_iterations(G1, A.saved_iterations)
plot_animations(G1, A.saved_iterations, 'outputs/with_gradient_backtrack_peterson.gif')

input("Press [enter] to finish.")




#CODE TO ANALYZE PRODUCED STRUCTURE