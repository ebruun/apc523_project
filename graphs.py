#PYTHON IMPORTS
import networkx as nx
from networkx.linalg.graphmatrix import incidence_matrix
import numpy as np
import matplotlib.pyplot as plt
import random

from scipy.spatial import ConvexHull, convex_hull_plot_2d

class Graph():

    def __init__(self, vertex_list, edge_list, **vars):
        
        self.dim = 2

        self.vertex_list = vertex_list
        self.edge_list = edge_list   

        if vars["edge_lengths"]:
            self.lengths = {values:vars["edge_lengths"][keys] for keys,values in edge_list.items()}
        else:
            self.lengths = self.calc_edge_len()

        if vars["rigid_edge"]:
            self.rigid_edge = vars["rigid_edge"]
            self.rigid_node = np.array([val for key,val in self.edge_list.items() if key in self.rigid_edge]).flatten()
        else:
            self.rigid_edge = None
            self.rigid_node = None

        self.G = self.create_graph(vars["features"])

    def create_graph(self, f):
        g = nx.Graph()

        g.add_nodes_from(self.vertex_list.keys(), color = f['n_color'])
        g.add_edges_from(self.edge_list.values(), color = f['e_color'][0], width = f['width'])

        u = [u for u,v in g.edges()]
        v = [v for u,v in g.edges()]
        for i,c in enumerate(f['e_color']):
            g[u[i]][v[i]]['color'] = c

        for n, p in self.vertex_list.items():
            g.nodes[n]['pos'] = p

        #make rigid edge plot thicker (assume only one such edge)
        if self.rigid_edge:
            g[self.rigid_node[0]][self.rigid_node[1]]['width'] = 5
            g.nodes[self.rigid_node[0]]['color'] ='r'
            g.nodes[self.rigid_node[1]]['color'] ='r'



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

    # mat = np.zeros([n,n])

    # mat[0,1] = 1
    # mat[1,0] = 1

    # mat[0,2] = 1
    # mat[2,0] = 1

    # mat[1,2] = 1
    # mat[2,1] = 1    

    for i in range(3,n):
        new_pnt = (round(random.random()*fac,1),round(random.random()*fac,1))
        points[i] = new_pnt

        #l = [idx for idx,x in enumerate(sum(mat) < 4) if x]
        # l2 = [x for x in l if x < i]

        l2 = [*range(0,i)]
        new_edges = random.sample(l2,2)

        edges[len(edges)] = (i,new_edges[0])
        edges[len(edges)] = (i,new_edges[1])

        # mat[i,new_edges[0]] = 1
        # mat[new_edges[0],i] = 1

        # mat[i,new_edges[1]] = 1
        # mat[new_edges[1],i] = 1

    return points, edges

def generate_graph_guess(vertex_list, fac = 1):

    n = len(vertex_list)

    points = {
        0: vertex_list[0],
        1: vertex_list[1],
    }

    for i in range(2,n):
        new_pnt = (round(random.random()*fac,1),round(random.random()*fac,1))
        points[i] = new_pnt

    return points



if __name__ == '__main__':
    generate_graph(10)
    