import numpy as np

class Hanning2D(object):
    """ 2D Hanning window. """

    def __init__(self, *args, **kwargs):
        """ Initialize object's internal data. """
        self.nofRows       = 0
        self.nofCols       = 0
        self.HanningColumn = []
        self.HanningRow    = []

