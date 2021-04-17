#PYTHON IMPORTS
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

import numpy as np


def plot(*args):

    plt.ion()

    fig, ax = plt.subplots(figsize=(9, 9))

    
    nx.draw(args[0].G, args[0].pos, with_labels=True, font_weight='bold',ax=ax)
    nx.draw(args[1].G, args[1].pos, with_labels=True, font_weight='bold', edge_color="r",ax=ax)
    
    limits=plt.axis('on') # turns on axis
    ax.set_xlim([-1, 5])
    ax.set_ylim([-10, 10])
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('equal')
    
    plt.show()
    plt.pause(0.001)
    input("Press [enter] to continue.")

    return fig,ax

def plot_update(g1,g2,i):
    ax = plt.gca()
    ax.clear()

    nx.draw(g1.G, g1.pos, with_labels=True, font_weight='bold', ax=ax)
    nx.draw(g2.G, g2.pos, with_labels=True, font_weight='bold', edge_color="r", ax=ax)

    ax.set_title('Iteration {}'.format(i))
    ax.set_xlim([-1, 5])
    ax.set_ylim([-10, 10])
    limits=plt.axis('on') # turns on axis
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.axis('equal')

    plt.show()
    plt.pause(0.01)
    #input("Press [enter] to continue.")

def plot_iterations(g1, saved):

    fig = plt.figure(figsize=(9, 9))

    for key, value in saved.items():
        print(key)
        ax = fig.add_subplot(2,2,key+1)
        ax.set_title("it. {}, Max Error = {:.2f}m ".format(key, value[1]))


        nx.draw(g1.G, g1.pos, with_labels=True, font_weight='bold', ax=ax)
        nx.draw(value[0].G, value[0].pos, with_labels=True, font_weight='bold',edge_color="r", ax=ax)

        ax.set_xlim([-1, 5])
        ax.set_ylim([-10, 10])
        limits=plt.axis('on') # turns on axis
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.axis('equal')

    plt.show()


def plot_animations(g1, saved):

    fig, ax = plt.subplots(figsize=(9, 9))

    def animate(i):
        ax.clear()
        nx.draw(g1.G, g1.pos, with_labels=True, font_weight='bold', ax=ax)
        nx.draw(saved[i][0].G, saved[i][0].pos, with_labels=True, font_weight='bold',edge_color="r", ax=ax)

        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        limits=plt.axis('on') # turns on axis

        ax.set_title("Iteration {}, Max. Abs. Error = {:.5f} m".format(i,saved[i][1]), fontweight="bold")

    anim = FuncAnimation(fig, animate,frames=len(saved), interval=500, repeat=True)

    anim.save('network_converge.gif', writer='imagemagick')

if __name__ == '__main__':
    plot_animations()
