# external dependencies
from numpy.linalg import inv
from numpy.linalg import norm
import matplotlib.pyplot as plt

# local functions from truss_element
from truss_element import setup
from truss_element import get_matrices
from truss_element import get_stresses
from truss_element import show_results

#PYTHON IMPORTS
import random

#LOCAL IMPORTS
from graphs import Graph, generate_graph
from graph_plot import plot, plot_iterations, plot_animations

from inputs.input_structure import p3, e3, p_validate, e_validate #pre-defined structures

##########################################################
# 1. Create target structure and properties.
##########################################################

# See predefined structures in the input_structure import above.
# Option 1:
vertices = p_validate
edges = e_validate

# Option 2:
# vertices = p3
# edges = e3

# Option 3, generate a random graph uncommenting the next 3 lines:
# random.seed(12)
# gen_size = 32 # Variations: 16, 32, 64, 128, 256, 512
# vertices, edges = generate_graph(n = gen_size, fac = 10)

# Units in the graph: meters
G1 = Graph(vertex_list = vertices, edge_list = edges)

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