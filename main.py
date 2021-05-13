#PYTHON IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import random
import networkx as nx
from autograd import value_and_grad

#LOCAL IMPORTS
from graphs import Graph, generate_graph, generate_graph_guess
from analysis import Analysis
from graph_plot import Plotter

#ANALYSIS STRUCTURE (TURN ONE ON)
from inputs.simple import data_in
#from inputs.medium_size import data_in
#from inputs.from_paper import data_in

##########################################################
# 1. Create target structure
##########################################################

# Turn on if want to generate a random structure
random.seed(20)
random_gen = False

if random_gen:
    # Random Initial Structure
    gen_size = 30
    vertices, edges = generate_graph(n = gen_size, fac = 5)
    lengths = []
    plotting_features = {'n_color':'#afcdfa','e_color': ['k'],'width': 2}
else:
    # Specified Initial Structure
    vertices = data_in["vertices"]
    edges = data_in["edges"]
    lengths = data_in["edge_lengths"]
    plotting_features = data_in["plotting_features1"]

G1 = Graph(
    vertex_list = vertices,
    edge_list = edges,
    edge_lengths = lengths,
    rigid_edge=[],
    features = plotting_features
    )


##########################################################
# 2. Set initial conditions
##########################################################

if random_gen:
    # Random Initial Guess
    vertices_guess = generate_graph_guess(vertex_list = vertices, fac = 5)
    rigid_edge = [0]
    plotting_features = {'n_color':'#ffbfd7','e_color': 'r','width': 2}
else:
    # Specified Initial Guess
    vertices_guess = data_in["initial_conditions"][0]
    rigid_edge = data_in["rigid_edge"]
    plotting_features = data_in["plotting_features2"]

G2 = Graph(
    vertex_list = vertices_guess,
    edge_list = edges,
    edge_lengths = [],
    rigid_edge = rigid_edge,
    features = plotting_features
    )


P = Plotter(G1, G2)
P.plot_initial(G1,G2) #Just G2 if not want to show target graph

input("\nPress [enter] to start analysis.")


##########################################################
# 3. Perform Multi-Dimensional Nonlinear Root Finding
##########################################################

if random_gen:
    # Random Initial Guess
    btrack = "peterson"
    n_max_steps = 30
    n_gradient_steps = 0
else:
    # Specified Initial Guess
    btrack = data_in["backtrack"]
    n_max_steps = data_in["n_max_steps"]
    n_gradient_steps = data_in["n_gradient_steps"]


A = Analysis(
    btrack = btrack,
    max_iter = n_max_steps,
    gradient_steps = n_gradient_steps,
    )

A.check_formulation(G1,G2)
A.iterator(G1,G2, P)


##########################################################
# 4. Output
##########################################################
if random_gen:
    output_vid = "outputs/rndm_{:.0f}_nodes__{:.0f}_gradsteps.gif".format(gen_size,n_gradient_steps)
elif data_in["name"] == "SimpleStructure":
    output_vid = data_in["output_vid"]
    P.error_plot(A.saved_iterations) #only for simple structure
else:
    output_vid = data_in["output_vid"]
    
P.plot_degree_distribution()    
P.plot_animations(A.saved_iterations,output_vid) #to make GIF

input("\nPress [enter] to finish.")
plt.close("all")




