#PYTHON IMPORTS
import numpy as np
from jax import value_and_grad

#LOCAL IMPORTS
from graph_plot import plot_update

class Analysis():

    def __init__(self, g, n=10):
        self.dim = 2

        self.n = n #iterations
        self.theta = np.array([val for key,val in g.pos.items() if key not in g.rigid_node]).flatten()

        self.abs_error_limit = 0.05
        self.rel_error_limit = 0.001

    def iterator(self,g1,g2):
        
        for i in range(self.n):

            print("\nIteration:", i)
            #print(g2.pos)
            
            J = np.zeros((g1.G.number_of_edges(),2*g1.G.number_of_nodes()))
            f_x = np.zeros(g1.G.number_of_edges())

            for num,edge in g2.edge_list.items():
                coords = self.find_coords(g2,edge) #current coordinates of edge
                L_target = g1.lengths[tuple(edge)] #correct length

                f_x[num],J[num,self.map_dof(edge)] = value_and_grad(self.calc_f_x,0)(coords,L_target) 
            
            J_red,f_x_red = self.reduce_jacobian(J,f_x,g2)

            #print("theta_old", self.theta)
            self.theta -= np.linalg.inv(J_red).dot(f_x_red)
            #print("theta_new", self.theta)

            self.update_pos(g2)

            plot_update(g1,g2,i)

            abs_error, edge_error = self.check_error(g1,g2)

            if abs_error < self.abs_error_limit:
                print("CONVERGED")
                break
            else:
                 print("NOT CONVERGED, largest error on {} : {} m".format(edge_error,abs_error))
            
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

    def check_error(self,g1,g2):
        
        g2.lengths = g2.calc_edge_len()

        max_abs_error = 0
        max_error_edge = (0,0)

        for edge,L in g2.lengths.items():
            L_target = g1.lengths[tuple(edge)] #correct length

            abs_error = abs(L-L_target)

            if abs_error > max_abs_error:
                max_abs_error = abs_error
                max_error_edge = edge
        
        return max_abs_error, max_error_edge