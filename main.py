#PYTHON IMPORTS
import matplotlib.pyplot as plt
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph, generate_graph_guess
from analysis import Analysis
from graph_plot import Plotter

#from inputs.simple import data_in
#from inputs.medium_size import data_in
from inputs.from_paper import data_in

##########################################################
# 1. Create target structure
##########################################################
# random.seed(12)
# gen_size = 20
# vertices, edges = generate_graph(n = gen_size, fac = 1)
# lengths = []

vertices = data_in["vertices"]
edges = data_in["edges"]
lengths = data_in["edge_lengths"]

G1 = Graph(
    vertex_list = vertices,
    edge_list = edges,
    edge_lengths = lengths,
    )


##########################################################
# 2. Set initial conditions
##########################################################
# vertices_guess = generate_graph_guess(n = gen_size, vertex_list = vertices, fac = 5)
# rigid_edge = [0]

vertices_guess = data_in["initial_conditions"][0]
rigid_edge = data_in["rigid_edge"]

G2 = Graph(
    vertex_list = vertices_guess,
    edge_list = edges,
    rigid_edge = rigid_edge,
    )

P = Plotter(G1)
P.plot_initial(G2)

input("Press [enter] to start analysis.")
plt.pause(1)


##########################################################
# 3. Perform Multi-Dimensional Nonlinear Root Finding
##########################################################
A = Analysis(btrack = "peterson", max_iter=100, gradient_steps = 5)
A.check_formulation(G1,G2)
A.iterator(G1,G2, P)


##########################################################
# 4. Output
##########################################################
#P.error_plot(A.saved_iterations) #for simple test case only
#P.plot_animations(A.saved_iterations,'outputs/simple.gif') #to make GIF

input("Press [enter] to finish.")
plt.pause(1)

#CODE TO ANALYZE PRODUCED STRUCTURE

