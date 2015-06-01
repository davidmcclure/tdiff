

from textplot.text import Text


class Matrix:


    @classmethod
    def from_paths(cls, p1, p2):

        """
        Build a matrix from a pair of file paths.

        Args:
            p1 (str)
            p2 (str)

        Returns: Matrix
        """

        return cls(Text.from_file(p1), Text.from_file(p2))


    def __init__(self, t1, t2):

        """
        Wrap a pair of text instances.

        Args:
            t1 (Text)
            t2 (Text)
        """

        self.t1 = t1
        self.t2 = t2
