

import networkx as nx

from textplot.text import Text
from clint.textui.progress import bar
from scipy.spatial import distance


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


    def kde_nn(self, n=500, **kwargs):

        """
        Match each term in t1 with the term in t2 with the most similar KDE.

        Args:
            n (int): Consider N most-frequent words.

        Returns:
            list: Tuples of (t1 term, t2 term, weight).
        """

        mft1 = self.text1.most_frequent_terms(n)
        mft2 = self.text2.most_frequent_terms(n)

        # For each term in text 1.
        links = []
        for t1 in mft1:

            st1 = self.text1.unstem(t1)

            # Score against each term in text 2.
            scores = []
            for t2 in mft2:

                st2 = self.text2.unstem(t2)

                t1_kde = self.text1.kde(t1, **kwargs)
                t2_kde = self.text2.kde(t2, **kwargs)

                score = 1-distance.braycurtis(t1_kde, t2_kde)
                scores.append((st2, score))

            # Register the closest match.
            scores = sorted(scores, key=lambda x: x[1], reverse=True)
            links.append((st1, scores[0][0], scores[0][1]))

        # Sort strongest -> weakest.
        links = sorted(links, key=lambda x: x[2], reverse=True)

        return links
