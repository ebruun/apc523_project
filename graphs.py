#PYTHON IMPORTS
import networkx as nx
import numpy as np
from jax import value_and_grad
import matplotlib.pyplot as plt

#LOCAL IMPORTS
from graph_plot import plot_update

class Graph():

    def __init__(self, pos = None, edge_list = None, rigid_edge = None):
        
        self.dim = 2

        if pos is None:
            self.pos = {
                0: (1, 1),
                1: (4, 1),
                2: (1, 5),
                3: (4, 5),
                }
        else:
            self.pos = pos
        
        if edge_list is None:   
            self.edge_list = {
                0: (0,1),
                1: (0,2),
                2: (0,3),
                3: (1,3),
                4: (2,3),
                } 
        else:
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

        g.add_nodes_from(self.pos.keys())
        g.add_edges_from(self.edge_list.values())

        for n, p in self.pos.items():
            g.nodes[n]['pos'] = p

        return g

    def calc_edge_len(self):
        lengths={}
        for edge in self.G.edges():
            start = np.array(self.pos[edge[0]])
            end = np.array(self.pos[edge[1]])

            lengths[edge] = np.linalg.norm(start-end)
        
        return lengths


class Analysis():

    def __init__(self, g, n=10):
        self.dim = 2

        self.n = n #iterations
        self.theta = np.array([val for key,val in g.pos.items() if key not in g.rigid_node]).flatten()

    def iterator(self,g1,g2):
        
        for i in range(self.n):

            print("\nNEW RUN")
            print(g2.pos)
            
            J = np.zeros((g1.G.number_of_edges(),2*g1.G.number_of_nodes()))
            f_x = np.zeros(g1.G.number_of_edges())

            for num,edge in g2.edge_list.items():
                coords = self.find_coords(g2,edge) #current coordinates of edge
                L_target = g1.lengths[tuple(edge)] #correct length

                f_x[num],J[num,self.map_dof(edge)] = value_and_grad(self.calc_f_x,0)(coords,L_target) 
            
            J_red,f_x_red = self.reduce_jacobian(J,f_x,g2)

            print("theta_old", self.theta)
            self.theta -= np.linalg.inv(J_red).dot(f_x_red)
            print("theta_new", self.theta)

            self.update_pos(g2)

            plot_update(g1,g2,i)

            
    def find_coords(self,g,edge):
        x_start, y_start = np.array(g.pos[edge[0]])
        x_end, y_end = np.array(g.pos[edge[1]])
        return np.array([x_start, y_start, x_end, y_end], dtype=float)

    def calc_f_x(self,x,L):
        x_start, y_start, x_end, y_end = x
        return (x_start - x_end)**2 + (y_start - y_end)**2 - L**2
    
    def map_dof(self,edge):
        return [edge[0]*self.dim, edge[0]*self.dim + 1, edge[1]*self.dim, edge[1]*self.dim + 1]

    def reduce_jacobian(self,J,f_x,g2):
        J_red = np.delete(J,g2.rigid_edge,axis=0) #column reduce

        col_red = []
        for node in g2.rigid_node:
            col_red.append([self.dim*node,self.dim*node+1])

        J_red = np.delete(J_red,col_red,axis=1) #row reduce

        f_x_red = np.delete(f_x, g2.rigid_edge)
        return J_red, f_x_red

    def update_pos(self,g2):
        count = 0
        for node,coord in g2.pos.items():
            if node not in g2.rigid_node:
                g2.pos[node] = (self.theta[count*self.dim], self.theta[count*self.dim + 1])
                count += 1