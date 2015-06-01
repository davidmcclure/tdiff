

from textplot.text import Text
from itertools import combinations
from scipy.spatial import distance
from scipy.misc import comb
from clint.textui.progress import bar


class Matrix:


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


    def compare(self, n, **kwargs):

        """
        Index KDE similarities between top N types in each text.

        Args:
            n (int): Consider top N words (by frequency) from each text.
        """

        mft1 = self.text1.most_frequent_terms(n)
        mft2 = self.text2.most_frequent_terms(n)

        terms = set.union(mft1, mft2)
        pairs = combinations(terms, 2)
        count = comb(len(terms), 2)

        links = []
        for t1 in mft1:

            st1 = self.text1.unstem(t1)

            scores = []
            for t2 in mft2:

                st2 = self.text2.unstem(t2)

                t1_kde = self.text1.kde(t1, **kwargs)
                t2_kde = self.text2.kde(t2, **kwargs)

                score = 1-distance.braycurtis(t1_kde, t2_kde)
                scores.append((st2, score))

            scores = sorted(scores, key=lambda x: x[1], reverse=True)

            if st1 != scores[0][0]:
                links.append((st1, scores[0][0], scores[0][1]))

        links = sorted(links, key=lambda x: x[2], reverse=True)
        return links
