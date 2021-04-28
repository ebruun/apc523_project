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

def main():
    """
    Main script for Finite Element analysis of a 2D truss structure.
    """
    # problem setup
    properties = setup()

    # determine global matrices
    K, R = get_matrices(properties)
    print('got matrices')
    # calculate static displacements of each element K*u = R
    # with numpy function
    u = inv(K).dot(R)
    print("K", K)
    print("u", u)
    print("R", R)

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
    show_results(u, stresses)

    plt.title('Analysis of Truss Structure')
    plt.show()

if __name__ == '__main__':
    main()