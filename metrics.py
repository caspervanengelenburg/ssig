import torch
import numpy as np
import networkx as nx


def iou_score(img1, img2, background = False):

    """
    Computes the Intersection-over-Union (IoU), or Jaccard Distance, between two semantic images.
    Inputs: query and key image; should be 2-D numpy arrays of the same shape.
    """

    # compute union
    union = (img1 < 12)
    union += (img2 < 12)

    # add background to union if needed
    if background:
        union += (img1 == 12)
        union += (img2 == 12)

    # intersection
    inter = (img1 - img2) == 0
    inter *= union

    # intersection-over-union
    return np.sum(inter) / np.sum(union)


def ged_score(g1, g2, normalize=True, ematch=True, nmatch=True):
    """
    Graph edit distance (GED),
    Can be normalized: / (sum_i {#nodes_i})
    Output: scalar (0, 1).
    """

    # Set GED matching strategy
    edge_match = lambda a, b: a['door'] == b['door'] if ematch else None
    node_match = lambda a, b: a['category'] == b['category'] if nmatch else None

    # compute graph-edit distance via NetworkX
    ged = nx.graph_edit_distance(g1, g2,
                                 edge_match=edge_match,
                                 node_match=node_match)

    # Normalize
    if normalize:
        ged /= (g1.number_of_nodes() * g2.number_of_nodes())

    return ged


def sged_score(g1, g2, ematch=True, nmatch=True):
    """
    Computes a normalized graph similarity score based on the
    Graph edit distance (GED). The GED is normalized first;
    an exponential of the negative is the final score.
    """

    # set GED matching strategy
    edge_match = lambda a, b: a['door'] == b['door'] if ematch else None
    node_match = lambda a, b: a['category'] == b['category'] if nmatch else None

    # compute graph edit distance (GED)
    ged = nx.graph_edit_distance(g1, g2,
                                 edge_match=edge_match,
                                 node_match=node_match)

    # output the similarity score of the normalized GED
    return np.exp(- 2 * ged / (g1.number_of_nodes() + g2.number_of_nodes()))


def ssig_score(miou, ged, gamma=0.4):
    """
    Computes SSIG based on the mean Intersection-over-Union (mIoU)
    and a graph distance based on the Graph Edit Distance (GED)
    between two floor plan samples. The distributions are weighted
    by a tweakable hyper-parameter, gamma. For RPLAN, gamma 0.4 provides
    an almost exact balance between mIoU and sGED distributions.
    """

    sged = np.power((1 - ged), gamma)

    return 0.5 * (miou + sged)