import torch
import numpy as np
import networkx as nx


def compute_iou(img_q, img_k, background=False):
    """
    Computes the Intersection-over-Union, or Jaccard Distance, between two semantic images.
    Inputs: query and key image; should be 2-D numpy arrays of the same shape.
    """

    # Compute
    union_area = (img_q < 12)
    union_area += (img_k < 12)
    if background:
        union_area += (img_q == 12)
        union_area += (img_k == 12)

    # Compute intersection
    inter_area = (img_q - img_k) == 0
    inter_area = inter_area * union_area

    # IoU
    return np.sum(inter_area) / np.sum(union_area)


# IoU between query image and a list or array of images
def get_ious(img_q, imgs, background=False):
    """
    Intersection-over-union between query and stack of key images.
    """

    # Initialize IoU vector
    n = imgs.shape[0]
    ious = np.zeros((n))

    # Compute IoU across full set of images
    for i in range(n):
        img_k = imgs[i]
        ious[i] = compute_iou(img_q, img_k, background=background)

    return ious


def mean_iou(pred_mask, mask, classes, smooth=1e-10):
    """
    Computes the mean Intersection-over-Union between two masks;
    the predicted multi-class segmentation mask and the ground truth.
    """

    n_classes = len(classes)

    # make directly equipable when training (set grad off)
    with torch.no_grad():

        pred_mask = pred_mask.contiguous().view(-1)
        mask = mask.contiguous().view(-1)

        iou_per_class = []
        for c in range(0, n_classes):  # loop over possible classes

            # compute masks per class
            true_class = pred_mask == c
            true_label = mask == c

            # when label does not exist in the ground truth, set to NaN
            if true_label.long().sum().item() == 0:
                iou_per_class.append(np.nan)
            else:
                intersect = torch.logical_and(true_class, true_label).sum().float().item()
                union = torch.logical_or(true_class, true_label).sum().float().item()

                iou = (intersect + smooth) / (union + smooth)
                iou_per_class.append(iou)

        return np.nanmean(iou_per_class)


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


def ssig_score(miou, sged, gamma=0.4):
    """
    Computes SSIG based on the mean Intersection-over-Union (mIoU)
    and a graph similarity based on the Graph Edit Distance (GED)
    between two floor plan samples. The distributions are weighted
    by a tweakable hyper-parameter, gamma. For RPLAN, gamma 0.4 provides
    an almost exact balance between mIoU and sGED distributions.
    """

    return 0.5 * (miou + np.power(sged, gamma))