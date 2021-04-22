#PYTHON IMPORTS
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import networkx as nx

import numpy as np


class Plotter():

    def __init__(self, g1):

        self.g1 = g1

        #self.fig_2, self.ax_2 = plt.subplots(figsize=(9, 9), num='Animation')
        self.fig_1, self.ax_1 = plt.subplots(figsize=(9, 9), num='Iterations')

        self.options1 = {
            'node_color': '#afcdfa',
            'node_size': 200,
            'edge_color':'black',
            'width': 2,
            #'ax':self.ax_1,
            'with_labels': True,
            'font_weight':'bold',
            }

        self.options2 = {
            'node_color': '#ffbfd7',
            'node_size': 200,
            'edge_color':'red',
            'width': 1,
            #'ax':self.ax_1,
            'with_labels': True,
            'font_weight':'bold',
            }

        self.options3 = {
            'node_color': '#ff3636',
            'node_size': 300,
            'edge_color':'#ff3636',
            'width': 5,
            #'ax':self.ax_1,
            'with_labels': True,
            'font_weight':'bold',
            }

    
    def plot_initial(self,g2):
        plt.ion()
        
        nx.draw(self.g1.G, pos = self.g1.vertex_list, ax=self.ax_1, **self.options1)
        nx.draw(g2.G, pos = g2.vertex_list,ax=self.ax_1, **self.options2)

        g2_rigid = g2.G.subgraph(g2.rigid_node)
        nx.draw(g2_rigid, pos = g2.vertex_list,ax=self.ax_1, **self.options3)
        
        self.ax_1.set_title('Starting Conditions')
        self.ax_1.set_xlim([-1, 5])
        self.ax_1.set_ylim([-10, 10])
        self.ax_1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        
        limits=plt.axis('on') # turns on axis
        plt.axis('equal')
        
        plt.show()
        input("Press [enter] to continue.")


    def plot_update(self,g2,i):
        self.ax_1.clear()

        nx.draw(self.g1.G, self.g1.vertex_list,ax=self.ax_1, **self.options1)
        nx.draw(g2.G, g2.vertex_list,ax=self.ax_1, **self.options2)

        g2_rigid = g2.G.subgraph(g2.rigid_node)
        nx.draw(g2_rigid, pos = g2.vertex_list,ax=self.ax_1, **self.options3)

        self.ax_1.set_title('Iteration {}'.format(i))
        self.ax_1.set_xlim([-1, 5])
        self.ax_1.set_ylim([-10, 10])
        self.ax_1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        
        limits=plt.axis('on') # turns on axis
        plt.axis('equal')

        plt.show()
        plt.pause(0.05)


    def plot_animations(self, saved, name):
        def animate(i):
            self.ax_1.clear()

            nx.draw(self.g1.G, self.g1.vertex_list, ax = self.ax_1, **self.options1, )
            nx.draw(saved[i][0].G, saved[i][0].vertex_list, ax = self.ax_1, **self.options2)

            g2_rigid = saved[i][0].G.subgraph(saved[i][0].rigid_node)
            nx.draw(g2_rigid, pos = saved[i][0].vertex_list,ax=self.ax_1, **self.options3)

            self.ax_1.set_title("Iteration {}, 0.5*sum|f(x)|^2 error  = {:.5f}".format(i,saved[i][1]), fontweight="bold")
            self.ax_1.set_xlim([-10, 20])
            self.ax_1.set_ylim([-10, 20])
            limits=plt.axis('on') # turns on axis
            self.ax_1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            
            plt.axis('equal')

        anim = FuncAnimation(self.fig_1, animate,frames=len(saved), interval=500, repeat=True)

        anim.save(name, writer='imagemagick')


    def error_plot(self, saved):

        x = np.linspace(-3, 10, 100)
        y = np.linspace(-8.5, 8.5, 100)

        X, Y = np.meshgrid(x, y)

        def f(x,y):
            return 0.5*(x**2 + y**2 - (4.5**2 + 7**2))**2 + 0.5*((x-5.5)**2 + y**2 - (1**2 + 7**2))**2

        func_vect = np.vectorize(f)

        Z = f(X, Y)


        fig1, ax1 = plt.subplots(figsize=(9, 9),subplot_kw={"projection": "3d"}, num = "Error")

        surf = ax1.plot_surface(X, Y, Z, 
            cmap='RdGy',
            linewidth=0,
            antialiased=False,
            )

        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('Error')
        ax1.set_title('Error surface for 2 DOF system')

        fig1.colorbar(surf, shrink=0.5, aspect=5)


        ###################
        fig2, ax2 = plt.subplots(figsize=(9, 9), num = "2D Error")

        surf2 = ax2.contourf(X, Y, Z, 
            50,
            cmap='RdGy',
            )
        
        #point_z = [1.20*value[1] for key, value in saved.items()]
        point_xy = [value[0].vertex_list[2] for key, value in saved.items()]
        point_xy = np.array(point_xy).T

        for i, txt in enumerate(point_xy[0]):
            ax2.annotate(i, (point_xy[0][i]+0.04, point_xy[1][i]))
        
        ax2.scatter(point_xy[0],point_xy[1],color="k",s=10, zorder=1)

        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('Gradient descent along error surface')
        ax2.autoscale(False) # To avoid that the scatter changes limits
        
        fig2.colorbar(surf2)


        plt.show()

# def plot_iterations(g1, saved):

#     fig = plt.figure(figsize=(9, 9))

#     for key, value in saved.items():
#         print(key)
#         ax = fig.add_subplot(2,2,key+1)
#         ax.set_title("it. {}, Max Error = {:.2f}m ".format(key, value[1]))


#         nx.draw(g1.G, g1.vertex_list, with_labels=True, font_weight='bold', ax=ax)
#         nx.draw(value[0].G, value[0].vertex_list, with_labels=True, font_weight='bold',edge_color="r", ax=ax)

#         ax.set_xlim([-1, 5])
#         ax.set_ylim([-10, 10])
#         limits=plt.axis('on') # turns on axis
#         ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
#         plt.axis('equal')

#     plt.show()