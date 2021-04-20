#PYTHON IMPORTS
import numpy as np
from autograd import value_and_grad
import copy

#LOCAL IMPORTS
from graph_plot import plot_update

class Analysis():

    def __init__(self, g, max_iter=10, btrack = False):
        self.dim = 2
        self.backtrack_on = btrack

        self.n = max_iter #iterations
        self.theta = np.array([val for key,val in g.vertex_list.items() if key not in g.rigid_node]).flatten()

        self.max_memb_err = 1e-6
        self.max_err = 1e-6
        self.rel_error_limit = 0.001

        self.saved_iterations = {}

        if btrack:
            self.btrack = btrack

    def iterator(self,g1,g2):

        self.saved_iterations[0] = (copy.deepcopy(g2), 0)
        L = self.find_lengths(g1,g2) #target lengths
        
        for i in range(self.n):

            print("\nIteration:", i)

            C = self.find_coords(g2) #coordinates of edges (as a 2x2 matrix)
            
            J = np.zeros((g1.G.number_of_edges(),2*g1.G.number_of_nodes()))
            f_x = np.zeros(g1.G.number_of_edges())

            for num,edge in g2.edge_list.items():
                coords = C[num].ravel()
                L_target = L[num]

                f_x[num],J[num,self.map_dof(edge)] = value_and_grad(self.calc_f_x,0)(coords,L_target) #0 means only coords tracked
            
            J_red,f_x_red = self.reduce_jacobian(J,f_x,g2)

            if i < 0:
                p = f_x_red.T.dot(J_red)
                p = (p / np.linalg.norm(p))
                alpha = 1.0
                err = 0.5*f_x_red.T.dot(f_x_red)
            else:
                p = np.linalg.inv(J_red).dot(f_x_red) #Newton step vector
                alpha, err = self.backtrack(g2, L, p, self.theta, f_x_red)
            
            self.theta -= alpha*p
            g2.vertex_list = self.update_pos(g2, self.theta)

            self.saved_iterations[i+1] = (copy.deepcopy(g2), err)

            max_memb_err, in_edge = self.err_member_len(g1,g2)
            
            #if max_memb_err < self.max_memb_err:
            if err < self.max_err:
                print("CONVERGED, 0.5*sum|f(x)|^2 = {:.3e}".format(err))
                break
            else:
                 print("NOT CONVERGED, 0.5*sum|f(x)|^2 = {:.3e}".format(err))
                 print("largest error on edge {} : {:.3e} m".format(in_edge,max_memb_err))
                 plot_update(g1,g2,i)
                 #input("Press [enter] to finish.")
    



    def find_coords(self,g2):
        a = [[g2.vertex_list[vertex] for vertex in edge] for _,edge in g2.edge_list.items()]
        return np.array(a)


    def find_lengths(self,g1,g2):
        a = [g1.lengths[tuple(edge)] for _,edge in g2.edge_list.items()]      
        return np.array(a)  


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


    def update_pos(self,g,x):
        """ take a reduced nodal position vector x and map to position dictionary
        
        x is in the form: [x0, y0, x1, y1,....xn, yn]
        
        """
        count = 0
        pos_temp = copy.deepcopy(g.vertex_list)

        for node,coord in g.vertex_list.items():
            if node not in g.rigid_node:
                pos_temp[node] = (x[count*self.dim], x[count*self.dim + 1])
                count += 1

        return pos_temp
        

    def err_member_len(self,g1,g2):
        """find maximum absolute length error"""

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


    def backtrack(self,g2, L, p, theta, f_x_start):
        """reduce the newton step until error is less than previous"""

        err1 = 0.5*f_x_start.T.dot(f_x_start)
        err2 = 0.5*f_x_start.T.dot(f_x_start)

        factor = 0
        #factor = 2e-4
        #factor = 0.29


        if self.backtrack_on:
            g = copy.deepcopy(g2)
            alpha = 1
            theta_start = copy.deepcopy(theta)
            theta = 0

            cnt = 0
            while err2 >= err1*(1 - alpha*factor):
                alpha = (1/2)**cnt
                theta = theta_start - alpha*p 

                g.vertex_list = self.update_pos(g, theta)

                C = self.find_coords(g)
                f_x = np.zeros(g.G.number_of_edges())

                for num,edge in g.edge_list.items():
                    coords = C[num].ravel()
                    L_target = L[num]

                    f_x[num] = self.calc_f_x(coords,L_target)

                err2 = 0.5*f_x.T.dot(f_x)
                print("--btrack, a = (1/2)^{}: sum|f(x)^2|*(1 - {}*a) = {:.2e}, sum|f(x+ap)^2| = {:.2e}".format(cnt, factor, err1*(1 - alpha*factor), err2))

                cnt = cnt + 1
            return alpha, err2
        else:
            return 1, err1