#PYTHON IMPORTS
import matplotlib.pyplot as plt
import networkx as nx


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