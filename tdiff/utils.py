

import networkx as nx


def dijkstra(graph, cutoff):

    """
    Compute the path distance between all nodes in a graph.

    Args:
        graph (nx.Graph)
        cutoff (int)

    Returns:
        A dictionary that maps node -> neighbors, sorted ascending. Eg:
        {
            'source1': [
                ('target1', 0.01),
                ('target2', 0.02),
                ...
            ],
            'source2': [
                ('target1', 0.01),
                ('target2', 0.02),
                ...
            ],
        }
    """

    # Get the pairwise path lenghts.
    dj = nx.all_pairs_dijkstra_path_length(graph, cutoff)

    distances = {}
    for source, targets in dj.items():

        # Sort targets from near -> distant.
        ordered = sorted(list(targets.items()), key=lambda x: x[1])
        distances[source] = ordered

    return distances
