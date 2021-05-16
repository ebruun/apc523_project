# Python imports
import random

# External dependencies.
from numpy.linalg import inv
import matplotlib.pyplot as plt

# Local functions from truss_element.
from truss_element import setup
from truss_element import get_matrices
from truss_element import get_stresses
from truss_element import show_results

# Graph inports.
from graphs import Graph, generate_graph
from inputs.medium_size import data_in

# Pre-defined structures.
from inputs.fem_input_structure import p3, e3, p_validate, e_validate

##########################################################
# 1. Create target structure and properties.
##########################################################

# See predefined structures in the input_structure import above.
option_1_validate = True
option_2 = False

# If options 1 and 2 are false, then run option 3 (a random graph)
if option_1_validate:
    vertices = p_validate
    edges = e_validate
    lengths = data_in["edge_lengths"]
    plotting_features = data_in["plotting_features1"]
elif option_2:
    vertices = p3
    edges = e3
    lengths = data_in["edge_lengths"]
    plotting_features = data_in["plotting_features1"]
else:
    # Option 3, generate a random graph:
    random.seed(12)
    gen_size = 32 # Variations: 16, 32, 64, 128, 256, 512
    lengths = []
    plotting_features = {'n_color':'#afcdfa','e_color': ['k'],'width': 2}
    vertices, edges = generate_graph(n = gen_size, fac = 10)

# Units in the graph: meters
G1 = Graph(
    vertex_list = vertices,
    edge_list = edges,
    edge_lengths = lengths,
    rigid_edge=[],
    features = plotting_features
    )

# Define force applied to last node of graph.
force_x = 0 # kN
force_y = -1000 # kN

# Define Modulus of Elasticity of all elements.
elasticity = 205e6 # kN/m2

# Define area of the cross-section of all elements.
area = 0.1 * 0.1 # m2

##########################################################
# 2. Run finite element analysis of a 2d truss structure.
##########################################################

def main():
    """
    Main script for Finite Element analysis of a 2D truss structure.
    """
    # problem setup
    properties = setup(G1, force_x, force_y, elasticity, area)

    # Global stiffness matrix and vector of forces
    K, R = get_matrices(properties)

    # Calculate static displacements of each element K*u = R
    # with numpy.linalg inv function
    u = inv(K).dot(R)

    # determine stresses in each element
    stresses = get_stresses(properties, u)

    # output results
    show_results(u, stresses, area)

    plt.title('Analysis of Truss Structure')
    plt.show()

if __name__ == '__main__':
    main()