#PYTHON IMPORTS
import numpy as np
from autograd import value_and_grad
import copy

class Analysis():

    def __init__(self, btrack = False, max_iter=10, gradient_steps = 0):
        
        self.name = "name_btrack_{}_grad{}".format(btrack,gradient_steps)
        
        self.dim = 2

        self.n = max_iter #iterations
        self.n_grad_steps = gradient_steps #iterations to start gradient

        self.max_memb_err = 1e-6
        self.max_abs_err = 1e-6
        self.max_rel_error = 1e-6

        self.err_save = 0

        self.saved_iterations = {}
        
        self.btrack = btrack

        
        
        
        
    def iterator(self,g1,g2, Plotter):

        L = self.lengths_to_array(g1,g2) #target lengths

        f_x, _ = self.calc_F(g2,L,autograd=False)
        err1 = self.err_cumulative(f_x)

        #starting
        self.saved_iterations[0] = (copy.deepcopy(g2), err1)
        self.theta = np.array([val for key,val in g2.vertex_list.items() if key not in g2.rigid_node]).flatten()
        
        for i in range(self.n):

            print("\nIteration:", i+1)

            f_x, J = self.calc_F(g2,L,autograd=True)
            J_red,f_x_red = self.reduce_jacobian(J,f_x,g2)

            if i < self.n_grad_steps:
                print("here")
                p = f_x_red.T.dot(J_red) #Gradient step vector
                alpha = self.backtrack(g2, L, p, self.theta, f_x)
            else:
                p = np.linalg.inv(J_red).dot(f_x_red) #Newton step vector
                alpha = self.backtrack(g2, L, p, self.theta, f_x)
            
            self.theta -= alpha*p

            g2.vertex_list = self.update_vertex_list(g2, self.theta)
            f_x, _ = self.calc_F(g2,L,autograd=False)

            err1 = self.err_cumulative(f_x)
            err1_rel = self.err_relative(err1)

            err2, in_edge = self.err_member_len(g1,g2)
            
            Plotter.plot_update(g2,i+1)
            self.saved_iterations[i+1] = (copy.deepcopy(g2), err1)

            if self.termination(err1, err1_rel, err2, in_edge) > 0:
                break

            #input("Press [enter] for next iteration.")

                 

    def calc_F(self,g,L,autograd = False):
        """calculate the value of the function, and the gradient if needed"""
        C = self.coords_to_array(g) #coordinates of edges (as a 2x2 matrix)
        
        J = np.zeros((g.G.number_of_edges(),2*g.G.number_of_nodes()))
        f_x = np.zeros(g.G.number_of_edges())

        for num,edge in g.edge_list.items():
            coords = C[num].ravel()
            L_target = L[num]

            if autograd:
                f_x[num],J[num,self.map_dof(edge)] = value_and_grad(self.calc_f_x,0)(coords,L_target) #0 means only coords tracked
            else:
                f_x[num] = self.calc_f_x(coords,L_target)    

        return f_x, J

    def calc_f_x(self,x,L):
        """individual function call"""
        x_start, y_start, x_end, y_end = x
        return (x_start - x_end)**2 + (y_start - y_end)**2 - L**2

    def coords_to_array(self,g2):
        a = [[g2.vertex_list[vertex] for vertex in edge] for _,edge in g2.edge_list.items()]
        return np.array(a)

    def lengths_to_array(self,g1,g2):
        a = [g1.lengths[tuple(edge)] for _,edge in g2.edge_list.items()]      
        return np.array(a)  



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


    def update_vertex_list(self,g,x):
        """ take a reduced nodal position vector x and map to position dictionary
        
        x is in the form: [x0, y0, x1, y1,....xn, yn]
        
        """
        count = 0
        pos_temp = g.vertex_list

        for node,coord in g.vertex_list.items():
            if node not in g.rigid_node:
                pos_temp[node] = (x[count*self.dim], x[count*self.dim + 1])
                count += 1

        return pos_temp
    


    def backtrack(self,g2, L, p, theta, f_x_start):
        """reduce the newton step until error is less than previous"""

        err1 = self.err_cumulative(f_x_start)
        err2 = err1

        alpha = 1

        if self.btrack:

            if self.btrack == "zero":
                factor = 0
            elif self.btrack == "armijo":
                factor = 2e-4
            elif self.btrack == "peterson":
                factor = 0.29

            g = copy.deepcopy(g2)

            theta_start = copy.deepcopy(theta)
            theta = 0

            cnt = 0
            while err2 >= err1*(1 - alpha*factor):
                alpha = (1/2)**cnt
                theta = theta_start - alpha*p 

                g.vertex_list = self.update_vertex_list(g, theta)

                f_x,_= self.calc_F(g,L,autograd=False)

                err2 = self.err_cumulative(f_x)
                print("--btrack, a = (1/2)^{}: 0.5*sum|f(x)^2|*(1 - {}*a) = {:.2e}, 0.5*sum|f(x+ap)^2| = {:.2e}".format(cnt, factor, err1*(1 - alpha*factor), err2))

                cnt += 1
        
        return alpha

#####################################

    def err_cumulative(self, f_x):
        """cumulative squared error for a vector"""
        return 0.5*f_x.T.dot(f_x)


    def err_relative(self, e):
        """check the different between iterations, set variable for next iteration"""
        diff = e - self.err_save
        self.err_save = e
        return abs(diff)


    def err_member_len(self,g1,g2):
        """find maximum absolute length error"""

        g2.lengths = g2.calc_edge_len()

        max_abs_error = 0
        max_abs_error_edge = (0,1)

        for edge,L in g2.lengths.items():
            L_target = g1.lengths[tuple(edge)] #correct length

            abs_error = abs(L-L_target)

            if abs_error > max_abs_error:
                max_abs_error = abs_error
                max_abs_error_edge = edge
        
        return max_abs_error, max_abs_error_edge


    def termination(self, err1, err1_rel, err2, in_edge):

        if err1 < self.max_abs_err and err1_rel < self.max_rel_error:
            print("CONVERGED AT ROOT")
            print("0.5*sum|f(x)|^2 = {:.3e}".format(err1))
            print("Relative error = {:.3e}".format(err1_rel))
            return 1
        elif err1_rel < self.max_rel_error:
            print("CONVERGED AT MINIMUM")
            print("0.5*sum|f(x)|^2 = {:.3e}".format(err1))
            print("Relative error = {:.3e}".format(err1_rel))
            print("largest error on edge {} : {:.3e} m".format(in_edge,err2))
            return 2                
        else:
            print("NOT CONVERGED")
            print("0.5*sum|f(x)|^2 = {:.3e}".format(err1))
            print("Relative error = {:.3e}".format(err1_rel))
            print("largest error on edge {} : {:.3e} m".format(in_edge,err2))
            return 0