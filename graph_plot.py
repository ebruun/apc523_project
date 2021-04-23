#PYTHON IMPORTS
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import networkx as nx

import numpy as np


class Plotter():

    def __init__(self, g1, g2):

        self.g1 = g1 #Goal structure
        self.g2 = g2 #Starting Guess
        
        self.fig_1, self.ax_1 = plt.subplots(figsize=(9, 9), num='Iterations')

        #starting condition
        self.options1 = {
            'node_color': [self.g1.G.nodes[u]['color'] for u in self.g1.G.nodes()],
            'node_size': 200,
            'edge_color':[self.g1.G[u][v]['color'] for u,v in self.g1.G.edges()],
            'width': [self.g1.G[u][v]['width'] for u,v in self.g1.G.edges()],
            'with_labels': True,
            'font_weight':'bold',
            }

        #iterations
        self.options2 = {
            'node_color': [self.g2.G.nodes[u]['color'] for u in self.g1.G.nodes()],
            'node_size': 200,
            'edge_color':[self.g2.G[u][v]['color'] for u,v in self.g2.G.edges()],
            'width': [self.g2.G[u][v]['width'] for u,v in self.g2.G.edges()],
            'with_labels': True,
            'font_weight':'bold',
            }

    
    def plot_initial(self,*g):
        plt.ion()
        
        if len(g)>1:
            nx.draw(g[0].G, pos = g[0].vertex_list, ax=self.ax_1, **self.options1)
            nx.draw(g[1].G, pos = g[1].vertex_list,ax=self.ax_1, **self.options2)
        else:
            nx.draw(g[0].G, pos = g[0].vertex_list, ax=self.ax_1, **self.options2)
        
        limits=plt.axis('on') # turns on axis
        self.ax_1.set_title('Starting Conditions')
        self.ax_1.set_xlabel('x', fontsize=20)
        self.ax_1.set_ylabel('y', fontsize=20)
        self.ax_1.set_xlim([-1, 5])
        self.ax_1.set_ylim([-10, 10])
        self.ax_1.tick_params(axis = 'x', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        self.ax_1.tick_params(axis = 'y', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.axis('equal')
        plt.grid()
        
        plt.show()



    def plot_update(self,i,*g):
        self.ax_1.clear()

        if len(g)>1:
            nx.draw(g[0].G, pos = g[0].vertex_list, ax=self.ax_1, **self.options1)
            nx.draw(g[1].G, pos = g[1].vertex_list,ax=self.ax_1, **self.options2)
        else:
            nx.draw(g[0].G, pos = g[0].vertex_list, ax=self.ax_1, **self.options2)

        limits=plt.axis('on') # turns on axis
        self.ax_1.set_title('Iteration {}'.format(i))
        self.ax_1.set_xlabel('x', fontsize=20)
        self.ax_1.set_ylabel('y', fontsize=20)
        self.ax_1.set_xlim([-1, 5])
        self.ax_1.set_ylim([-10, 10])
        self.ax_1.tick_params(axis = 'x', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        self.ax_1.tick_params(axis = 'y', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.axis('equal')
        plt.grid()

        plt.show()
        plt.pause(0.05)


    def plot_animations(self, saved, name):
        def animate(i):
            self.ax_1.clear()

            nx.draw(self.g1.G, self.g1.vertex_list, ax = self.ax_1, **self.options1, )
            nx.draw(saved[i][0].G, saved[i][0].vertex_list, ax = self.ax_1, **self.options2)

            self.ax_1.set_title("Iteration {}, 0.5*sum|f(x)|^2 error  = {:.5f}".format(i,saved[i][1]), fontweight="bold")
            self.ax_1.set_xlabel('x', fontsize=20)
            self.ax_1.set_ylabel('y', fontsize=20)            
            self.ax_1.set_xlim([-10, 20])
            self.ax_1.set_ylim([-10, 20])
            self.ax_1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            
            limits=plt.axis('on') # turns on axis 
            plt.axis('equal')
            plt.grid()

        anim = FuncAnimation(self.fig_1, animate,frames=len(saved), interval=500, repeat=True)

        anim.save(name, writer='imagemagick')


    def error_plot(self, saved):
        """visualizing the simple 3-noded structure error surface
        
        This is hard-coded for the 3-noded structure, do not use for others
        """

        x = np.linspace(-3, 10, 100)
        y = np.linspace(-8.5, 8.5, 100)

        X, Y = np.meshgrid(x, y)

        def f(x,y):
            return 0.5*(x**2 + y**2 - (4.5**2 + 7**2))**2 + 0.5*((x-5.5)**2 + y**2 - (1**2 + 7**2))**2

        func_vect = np.vectorize(f)

        Z = f(X, Y)

        ######################################
        # 1st Plot: 3D surface
        ######################################

        fig1, ax1 = plt.subplots(figsize=(9, 9),subplot_kw={"projection": "3d"}, num = "Error")

        surf = ax1.plot_surface(X, Y, Z, 
            cmap='RdGy',
            linewidth=0,
            antialiased=False,
            )

        ax1.set_xlabel('x', fontsize=20)
        ax1.set_ylabel('y', fontsize=20)
        ax1.set_zlabel('Error', fontsize=20)
        ax1.set_title('Error surface for 2 DOF system')

        fig1.colorbar(surf, shrink=0.5, aspect=5)


        ######################################
        # 2nd Plot: 2D contours
        ######################################
        fig2, ax2 = plt.subplots(figsize=(9, 9), num = "2D Error")

        #levels = np.linspace(-1000,6500,40)
        surf2 = ax2.contourf(X, Y, Z, 
            70,
            #levels = levels,
            cmap='RdGy',
            )
        
        #point_z = [1.20*value[1] for key, value in saved.items()]
        point_xy = [value[0].vertex_list[2] for key, value in saved.items()]
        point_xy = np.array(point_xy).T

        for i, txt in enumerate(point_xy[0][0:6]):
            ax2.annotate(i, (point_xy[0][i]+0.04, point_xy[1][i]), fontsize=20, color='white')
        
        ax2.scatter(point_xy[0],point_xy[1],color="blue",s=15, zorder=1)

        ax2.set_xlabel('x', fontsize=20)
        ax2.set_ylabel('y', fontsize=20)
        ax2.tick_params(axis = 'x', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        ax2.tick_params(axis = 'y', labelsize=15, left=True, bottom=True, labelleft=True, labelbottom=True)
        ax2.set_title('Gradient descent along error surface')
        ax2.autoscale(False) # To avoid that the scatter changes limits
        
        fig2.colorbar(surf2)

        plt.show()
