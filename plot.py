import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import cv2


# custom figure set up
def set_figure(nc, nr,
               fs=10,
               fs_title=7.5,
               fs_legend=10,
               fs_xtick=3,
               fs_ytick=3,
               fs_axes=4,
               ratio=1):
    """
    Custom figure setup function that generates a nicely looking figure outline.
    It includes "making-sense"-fontsizes across all text locations (e.g. title, axes).
    You can always change things later yourself through the outputs or plt.rc(...).
    """

    fig, axs = plt.subplots(nc, nr, figsize=(fs*nr*ratio, fs*nc))

    try:
        axs = axs.flatten()
    except:
        pass

    plt.rc("figure", titlesize=fs*fs_title)
    plt.rc("legend", fontsize=fs*fs_legend)
    plt.rc("xtick", labelsize=fs*fs_xtick)
    plt.rc("ytick", labelsize=fs*fs_ytick)
    plt.rc("axes", labelsize=fs*fs_axes, titlesize=fs*fs_title)

    return fig, axs


# plot the access (and adjacency) graph of a floor plan
def plot_graph(G, ax,
               c_node='black', c_edge='black',  # coloring
               dw_edge=False, pos=None,  # edge type and node positioning
               node_size=10, edge_size=10):  # node and edge sizes

    """
    Plots the topological access (and potentially adjacency) graph structure of a floor plan:
    - Nodes are (/can be) colored based on the room type
    - Edges are (/can be) 'colored' based on the edge type: full for 'door', dashed for 'adjacent-only'
    - Node positions are (/can be) manually set e.g. by the centroid of the room (otherwise random spring layout)
    """

    # Determine node position (if None is given)
    if pos is None:
        pos = nx.spring_layout(G, seed=7)  # random position for the nodes

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=c_node, ax=ax)

    # Draw edges
    if dw_edge:

        # Door connections
        edges = [(u, v) for (u, v, d) in G.edges(data=True) if d["door"]]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=c_edge,
                               width=edge_size, ax=ax)

        # Adjacent connections
        edges = [(u, v) for (u, v, d) in G.edges(data=True) if not d["door"]]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=c_edge,
                               width=edge_size, style="dashed", ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, edge_color=c_edge,
                               width=edge_size, ax=ax)

    ax.axis('off')


# helper functions

# plot a polygon
def plot_polygon(ax, poly, label=None, **kwargs):
    x, y = poly.exterior.xy
    ax.fill(x, y, label=label, **kwargs)
    return


# convert an image from torch default to numpy default
def convert_img(img, mean=0.5, std=0.5):
    # image to numpy array (make sure to clone and detach)
    img = img.cpu().clone().detach().numpy()
    # swap around dimensions: color should be in the back (3rd dimension instead of 1st)
    img = img.transpose(1,2,0)
    # transform the image to have mean and std similar to before
    img = np.array([mean, mean, mean]) + img*np.array([std, std, std])
    img = img.clip(0, 1)
    return img