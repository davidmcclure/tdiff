

import networkx as nx

from collections import OrderedDict
from textplot.utils import sort_dict


def dijkstra(graph, cutoff):

    """
    Compute the path distance between all nodes in a graph.

    Args:
        graph (nx.Graph)
        cutoff (int)

    Returns:
        dict: A map of node (str) -> neighbors (OrderedDict).
    """

    # Get source -> target distances.
    distances = nx.all_pairs_dijkstra_path_length(graph, cutoff)

    # Order the targets by distance.
    for source, targets in distances.items():
        distances[source] = sort_dict(targets, desc=False)

    return distances
