import os
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
import torch_geometric


# Loading and unloading pickled files
def save_pickle(object, filename):
    """
    Saves a pickled file.
    """
    with open(filename, 'wb') as f:
        pickle.dump(object, f)
    f.close()


def load_pickle(filename):
    """
    Loads a pickled file.
    """
    with open(filename, 'rb') as f:
        object = pickle.load(f)
        f.close()
    return object


# RPLAN image loading
def load_image_rplan(id, data_path):
    img_path = os.path.join(data_path, 'original', f'{id}.png')
    img = (255*plt.imread(img_path)[..., 1]).astype(int)
    return img


# Floor plan colorization
def colorize_floorplan(img, classes, cmap):

    """
    Colorizes an integer-valued image (multi-class segmentation mask)
    based on a map of classes and colormap.
    """

    h, w = np.shape(img)
    img_c = (np.ones((h, w, 3)) * 255).astype(int)
    for cat in classes:
        color = np.array(cmap(cat))[:3] * 255
        img_c[img == cat, :] = color.astype(int)

    return img_c


# Graph-based utilities
def pyg_to_nx(graph, node_attrs=None, edge_attrs=None, graph_attrs=None):
    """
    Creates a networkx graph from a pytorch geometric graph data structure
    :param edge_attrs: transferred edge attributes
    :param node_attrs: transferred node attributes
    :param graph: a pytorch geometric graph structure
    :return: graph with fewer node and edge categories
    """
    if graph_attrs is None:
        graph_attrs = []
    if node_attrs is None:
        node_attrs = []
    if edge_attrs is None:
        edge_attrs = []
    return torch_geometric.utils.to_networkx(graph, to_undirected=True,
                                             node_attrs=node_attrs,
                                             edge_attrs=edge_attrs,
                                             graph_attrs=graph_attrs)


def simple_graph(graph):
    """
    Creates simple graph with reduced node and edge attributes.
    Remaining node attributes: categorical room types. Should be called 'category'.
    Remaining edge attributes: door types. Should be called 'door'
    """

    # Creates simple Networkx graph with only 'category' and 'door' attributes.
    graph = torch_geometric.utils.to_networkx(graph,
                                              to_undirected=True,
                                              node_attrs=['category'],
                                              edge_attrs=['door'])

    return graph


def remove_attributes_from_graph(graph, list_attr=None):
    """
    Removes attributes from graph.
    :param graph: Input topological graph.
    :param list_attr: Attributes to-be removed.
    :return: Output topological graph with removed attributes.
    """

    if list_attr is None:
        list_attr = ['polygons']
    for attr in list_attr:
        for n in graph.nodes(): # delete irrelevant nodes
            del graph.nodes[n][attr]
    return graph


# gather IDs
def gather_ids(ids_path='./data/valid_ids.pickle', shuffle=True):
    ids = load_pickle(ids_path)['full'].tolist()
    if shuffle: random.Random(4).shuffle(ids)
    return ids