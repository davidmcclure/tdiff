

import networkx as nx
import editdistance

from collections import OrderedDict
from clint.textui.progress import bar
from scipy.spatial import distance
from textplot.helpers import build_graph
from textplot.utils import sort_dict
from tdiff.text import Text
from tdiff.utils import dijkstra


class Diff:


    @classmethod
    def from_paths(cls, path1, path2):

        """
        Build a matrix from a pair of file paths.

        Args:
            path1 (str)
            path2 (str)

        Returns: Matrix
        """

        return cls(Text.from_file(path1), Text.from_file(path2))


    def __init__(self, text1, text2):

        """
        Wrap a pair of text instances.

        Args:
            text1 (Text)
            text2 (Text)
        """

        self.text1 = text1
        self.text2 = text2


    def kde_best_match(self, n=500, show_matches=False, **kwargs):

        """
        For each term in text 1, find the term in text 2 with the most similar
        pattern of distribution.

        Args:
            n (int): Consider N most-frequent words.
            show_matches (bool): Show identity (A -> A) matches.

        Returns:
            list: Tuples of (t1 term, t2 term, weight).
        """

        mft1 = self.text1.most_frequent_terms(n)
        mft2 = self.text2.most_frequent_terms(n)

        # For each term in text 1.
        links = []
        for t1 in mft1:

            # Score against each term in text 2.
            scores = []
            for t2 in mft2:

                t1_kde = self.text1.kde(t1, **kwargs)
                t2_kde = self.text2.kde(t2, **kwargs)

                score = 1-distance.braycurtis(t1_kde, t2_kde)
                scores.append((t2, score))

            # Get the nearest neighbor.
            scores = sorted(scores, key=lambda x: x[1], reverse=True)
            t2 = scores[0][0]

            if show_matches or t1 != t2:
                links.append((
                    self.text1.unstem(t1),
                    self.text2.unstem(t2),
                    scores[0][1]
                ))

        # Sort strongest -> weakest.
        links = sorted(links, key=lambda x: x[2], reverse=True)

        return links


    def topn_edit_distances(self, term_depth=500, n=10, **kwargs):

        """
        For each term in text 1, find the term in text 2 with the most similar
        set of nearest-neighbors, in terms of path distance.

        Args:
            n (int): The number of neighbors to consider.

        Returns:
            list: Tuples of (t1 term, t2 term, distance)
        """

        # Build graphs.
        g1 = self.text1.build_graph(term_depth=term_depth, **kwargs)
        g2 = self.text2.build_graph(term_depth=term_depth, **kwargs)

        # Get lengths between all pairs.
        dj1 = dijkstra(g1.graph, cutoff=n)
        dj2 = dijkstra(g2.graph, cutoff=n)

        # For each term in text 1.
        links = []
        for s1, t1 in bar(dj1.items()):

            # Score against each term in text 2.
            scores = OrderedDict()
            for s2, t2 in dj2.items():

                nn1 = list(t1.keys())[:n]
                nn2 = list(t2.keys())[:n]
                scores[s2] = editdistance.eval(nn1, nn2)

            # Get the closest neighbor.
            scores = sort_dict(scores, desc=False)
            winner = list(scores.items())[0]

            # Register the match.
            links.append((s1, winner[0], winner[1]))

        # Sort strongest -> weakest.
        links = sorted(links, key=lambda x: x[2])

        return links


    def topn_digraph(self, term_depth=500, skim_depth=5, **kwargs):

        """
        For each term in text 1, find the N most similar terms in text 2 and
        register the connections as edges in a digraph. Then, do the same thing
        in the opposite direction, linking text 2 "back" onto text 1.

        Args:
            n (int): The number of neighbors to consider.

        Returns: nx.DiGraph
        """

        pass
