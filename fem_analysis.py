# external dependencies
from numpy.linalg import inv
from numpy.linalg import norm
import matplotlib.pyplot as plt
from scipy.sparse.linalg import dsolve
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import bicg

# local functions from truss_element
from truss_element import setup
from truss_element import get_matrices
from truss_element import get_stresses
from truss_element import show_results

#PYTHON IMPORTS
import random

#LOCAL IMPORTS
from graphs import Graph
from graph_plot import plot, plot_iterations, plot_animations

from inputs.input_structure import p3, e3, p_validate, e_validate #pre-defined structures


##########################################################
# 1. Create target structure and properties.
##########################################################
gen_size = 6

vertices = p_validate
edges = e_validate

# meters
G1 = Graph(vertex_list = vertices, edge_list = edges)

force_x = 0 # kN
force_y = -1000 # kN
elasticity = 205e6 # kN/m2
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

    # determine global matrices
    K, R = get_matrices(properties)

    # calculate static displacements of each element K*u = R
    # with numpy function
    u = inv(K).dot(R)

    # with scipy spsolve
    # K_matrix = csc_matrix(K)
    # u_dsolve = dsolve.spsolve(K_matrix, R, use_umfpack=False)
    # print("u_dsolve", u_dsolve)

    # # with scipy bicg
    # u_bicg, _ = bicg(K, R)
    # print("u_bicg", u_bicg)

    # determine stresses in each element
    stresses = get_stresses(properties, u)

    # output results
    show_results(u, stresses, area)

    plt.title('Analysis of Truss Structure')
    plt.show()

if __name__ == '__main__':
    main()