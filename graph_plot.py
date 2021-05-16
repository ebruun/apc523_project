#PYTHON IMPORTS
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx


class Plotter():

    def __init__(self, g1):

        self.g1 = g1

        self.fig_2, self.ax_2 = plt.subplots(figsize=(9, 9))
        self.fig_1, self.ax_1 = plt.subplots(figsize=(9, 9))

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

    
    def plot_initial(self,g2):
        plt.ion()
        
        nx.draw(self.g1.G, self.g1.vertex_list, ax=self.ax_1, **self.options1)
        nx.draw(g2.G, g2.vertex_list,ax=self.ax_1, **self.options2)
        
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
            self.ax_2.clear()

            nx.draw(self.g1.G, self.g1.vertex_list, ax = self.ax_2, **self.options1, )
            nx.draw(saved[i][0].G, saved[i][0].vertex_list, ax = self.ax_2, **self.options2)

            self.ax_2.set_title("Iteration {}, 0.5*sum|f(x)|^2 error  = {:.5f}".format(i,saved[i][1]), fontweight="bold")
            self.ax_2.set_xlim([-10, 20])
            self.ax_2.set_ylim([-10, 20])
            limits=plt.axis('on') # turns on axis
            self.ax_2.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            
            plt.axis('equal')

        anim = FuncAnimation(self.fig_2, animate,frames=len(saved), interval=500, repeat=True)

        anim.save(name, writer='imagemagick')



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