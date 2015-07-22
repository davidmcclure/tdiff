

from textplot.text import Text as BaseText
from textplot.matrix import Matrix
from textplot.graphs import Skimmer


class Text(BaseText):


    def build_graph(self, term_depth=1000, skim_depth=10,
                    terms=None, **kwargs):

        """
        Construct a term graph.

        Args:
            term_depth (int): Consider the N most frequent terms.
            skim_depth (int): Connect each word to the N closest siblings.
            terms (list): Use a custom set of terms.

        Returns:
            textplot.graphs.Skimmer
        """

        # By default, use N most-frequent terms.
        terms = terms or self.most_frequent_terms(term_depth)

        # Index the term matrix.
        m = Matrix()
        m.index(self, terms, **kwargs)

        # Construct the network.
        g = Skimmer()
        g.build(self, m, skim_depth)

        return g
