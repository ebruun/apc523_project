#PYTHON IMPORTS
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

from scipy.spatial import ConvexHull, convex_hull_plot_2d

class Graph():

    def __init__(self, vertex_list, edge_list, rigid_edge = None):
        
        self.dim = 2

        self.vertex_list = vertex_list
        self.edge_list = edge_list   

        if rigid_edge is None:
            self.rigid_edge = None
            self.ridid_node = None
        else:
            self.rigid_edge = rigid_edge
            self.rigid_node = np.array([val for key,val in self.edge_list.items() if key in self.rigid_edge]).flatten()

        self.G = self.create_graph()
        self.lengths = self.calc_edge_len()

    def create_graph(self):
        g = nx.Graph()

        g.add_nodes_from(self.vertex_list.keys())
        g.add_edges_from(self.edge_list.values())

        for n, p in self.vertex_list.items():
            g.nodes[n]['pos'] = p

        return g

    def calc_edge_len(self):
        lengths={}
        for edge in self.edge_list.values():
            start = np.array(self.vertex_list[edge[0]])
            end = np.array(self.vertex_list[edge[1]])

            lengths[edge] = np.linalg.norm(start-end)
        
        return lengths


def generate_graph(n = 10, fac = 1):

    """generate a random graph but start with a triangle"""
    
    # points = np.random.rand(30, 2)
    # hull = ConvexHull(points)

    # plt.plot(points[:,0], points[:,1], 'o')

    # for simplex in hull.simplices:
    #     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    # plt.show()

    #starting conditions
    #points = np.array([[0,0],[3,0],[1.5,1.5]])
    #edges = np.array([[0,1],[0,2],[1,2]])

    points = {
        0: (0,0),
        1: (3,0),
        2: (1.5,1.5),
        }

    edges = {
        0: (0,1),
        1: (0,2),
        2: (1,2),
        }

    for i in range(3,n):
        new_pnt = (round(random.random()*5,1),round(random.random()*5,1))
        points[i] = new_pnt

        l = [*range(0,i)]
        new_edges = random.sample(l,2)

        edges[len(edges)] = (i,new_edges[0])
        edges[len(edges)] = (i,new_edges[1])

    return points, edges



if __name__ == '__main__':
    generate_graph(10)
    