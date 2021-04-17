import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt


def setup():
    """
    Setup geometry, material, boundary conditions, loads, cross-section.
    """
    # define coordinate system
    x_axis = np.array([1.0, 0.0])
    y_axis = np.array([0.0, 1.0])

    # define model
    nodes = {1: [0.0, 10.0], 2: [0.0, 0.0], 3: [10.0, 5.0]}
    dof = {1: [1, 2], 2: [3, 4], 3: [5, 6]}
    elements = {1: [1, 3], 2: [2, 3]}
    restrained_dof = [1, 2, 3, 4]
    forces = {1: [0.0, 0.0], 2: [0.0, 0.0], 3: [0.0, -200.0]}

    # material properties: Steel
    stiffnesses = {1: 30.0e6, 2: 30.0e6}

    # geometric properties
    areas = {1: 1.0, 2: 2.0}

    ndof = 2 * len(nodes)

    return {'x_axis': x_axis, 'y_axis': y_axis, 'nodes': nodes,
            'dof': dof, 'elements': elements, 'restrained_dof': restrained_dof,
            'forces': forces, 'ndof': ndof, 'stiffnesses': stiffnesses,
            'areas': areas}

def plot_nodes(nodes):
    """
    Plot nodes with global enumeration.
    """
    x = [i[0] for i in nodes.values()]
    y = [i[1] for i in nodes.values()]
    size = 400
    offset = size/4000
    plt.scatter(x, y, c='y', s=size, zorder=5)

    for i, location in enumerate(zip(x, y)):
        plt.annotate(i+1, (location[0]-offset,  location[1]-offset), zorder=10)

def points(element, properties):
    """
    Get start and end points of an element, and respective degrees of freedom.
    """
    elements = properties['elements']
    nodes = properties['nodes']
    dof = properties['dof']

    # find nodes that elements connects
    start_node = elements[element][0]
    end_node = elements[element][1]

    # coordinates for each node
    start_pt = np.array(nodes[start_node])
    end_pt = np.array(nodes[end_node])

    # degrees of freedom for each node
    dof_nodes = dof[start_node] # get the first 2 dof from start node
    dof_nodes.extend(dof[end_node]) # add 2 dof from end node and flatten list
    dof_nodes = np.array(dof_nodes)

    return start_pt, end_pt, dof_nodes

def draw_element(start_pt, end_pt, element, areas):
    """
    Draw an element with linewidth proportional to it's cross-section area.
    """
    plt.plot([start_pt[0], end_pt[0]], [start_pt[1], end_pt[1]], color='g',
            linestyle='-', linewidth=7*areas[element], zorder=1)

def direction_cosine(vec1, vec2):
    """
    Get the direction cosine (the cosine of the angle between two vectors).
    """
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def rotation_matrix(element_vec, x_axis, y_axis):
    """
    Rotation matrix of an element.
    """
    x_proj = direction_cosine(element_vec, x_axis)
    y_proj = direction_cosine(element_vec, y_axis)

    return np.array([[x_proj, y_proj, 0, 0],[0, 0, x_proj, y_proj]])

def get_matrices(properties):
    """
    """
    # construct the global stiffness matrix
    ndof = properties['ndof']
    nodes = properties['nodes']
    elements = properties['elements']
    forces = properties['forces']
    areas = properties['areas']
    x_axis = properties['x_axis']
    y_axis = properties['y_axis']

    plot_nodes(nodes)
    print(ndof)
    K = np.zeros((ndof, ndof))

    for element in elements:
        # find element geometry
        start_pt, end_pt, dof = points(element, properties)
        element_vec = end_pt - start_pt
        draw_element(start_pt, end_pt, element, areas)

        # local element stiffness matrix
        length = norm(element_vec)
        area = properties['areas'][element]
        E = properties['stiffnesses']

        c_k = E[element] * area / length

        k_element = np.array([[1, -1], [-1, 1]])

        # element rotation matrix
        q_element = rotation_matrix(element_vec, x_axis, y_axis)
        # apply rotation
        k_q = q_element.T.dot(k_element).dot(q_element)

        # change from element to global coord.
        index = dof - 1
        Q = np.zeros((4, ndof))
        for i in range(4):
            Q[i, index[i]] = 1.0

        K_q = Q.T.dot(k_q).dot(Q)
        K += c_k * K_q

    # force vector R
    R = []
    for r in forces.values():
        R.extend(r)
    R = np.array(R)

    # remove restrained dof (the rows and cols of K we need to delete)
    remove_indices = np.array(properties['restrained_dof']) - 1
    for i in [0, 1]:
        K = np.delete(K, remove_indices, axis=i)

    R = np.delete(R, remove_indices)

    return K, R

def get_stresses(properties, u):
    """
    Stress in each element.
    """
    x_axis = properties['x_axis']
    y_axis = properties['y_axis']
    elements = properties['elements']
    E = properties['stiffnesses']

    # find stresses in each element in local coord.
    stresses = []
    for element in elements:
        # find element geometry
        start_pt, end_pt, dof = points(element, properties)
        element_vec = end_pt - start_pt

        # element rotation matrix
        q_element = rotation_matrix(element_vec, x_axis, y_axis)
        u_global = np.array([0, 0, u[0], u[1]]) # only axial displacements
        u_element = q_element.dot(u_global)

        strain = (u_element[1] - u_element[0]) / norm(element_vec)
        stress = E[element] * strain
        stresses.append(stress)

    return stresses

def show_results(u, stresses):
    """
    """
    print("Nodal Displacments:", u)
    print("Stresses:", stresses)
    print("Displacment Magnitude:", round(norm(u), 5))
    print("\n")


def main():
    """
    Main script.
    """
    # problem setup
    properties = setup()

    # determine global matrices
    K, R = get_matrices(properties)

    # calculate static displacements of each element
    u = np.linalg.inv(K).dot(R)

    # determine stresses in each element
    stresses = get_stresses(properties, u)

    # output results
    show_results(u, stresses)

    plt.title('Analysis of Truss Structure')
    plt.show()

if __name__ == '__main__':
    main()