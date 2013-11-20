import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## =============================================================================
##
##  Helper functions
##
## =============================================================================

def Sin (x,
         a0=0.0,
         a1=1.0,
         a2=1.0,
         a3=0.0):
    """ Generalized sin function, including offsets and scale factors.
    """
    return a0+a1*np.sin(a2*x+a3)

## =============================================================================
##
##  Class definition
##
## =============================================================================

class Data(object):
    """ Data object to facilitate passing around input and generated data.
    """
    def __init__(self, *args, **kwargs):
        """ Initialize object's internal data.
        """

        """Image area for full CCD. """
        self.image_area = (1024,600)
        """ Image area selection slices. """
        self._selection = [ slice(100,500), slice(200,500) ]
        """ Detector signal for full CCD. """
        self._lx_data = np.random.rand(self.image_area[0],self.image_area[1])
        """ Pixel quality mask for full CCD. """
        self.pixel_quality = []
        """ Masked array for the signal array. """
        self.signal_masked = []
        """ Masked array for the selection from the signal array. """
        self.signal_selection_masked = []
        """ Row normalization factor. Must be floating point to yield non-zero
            values later on. """
        self.f_norm_row = np.zeros(self._selection[0].stop-self._selection[0].start, 'float32')
        """ Column normalization factor. Must be floating point to yield non-zero
            values later on. """
        self.f_norm_col = np.zeros(self._selection[1].stop-self._selection[1].start, 'float32')
        """ Row number index for selection. """
        self.index_row = np.arange(self._selection[0].start, self._selection[0].stop, 1)
        """ Column number index for selection. """
        self.index_col = np.arange(self._selection[1].start, self._selection[1].stop, 1)
        """ Row normalized detector signal. """
        self._signal_row_norm = np.ndarray(shape=(len(self.index_row),self.image_area[1]), dtype=float)
        """ Spectral calibration map (SCM). """
        self._scm = []

    def setSelection (self, selection):
        """ Set image area selection.
        """
        if len(selection)==2:
            self._selection = selection
            self.f_norm_row = np.zeros(self._selection[0].stop-self._selection[0].start, 'float32')
            self.f_norm_col = np.zeros(self._selection[1].stop-self._selection[1].start, 'float32')
            self.index_row = np.arange(self._selection[0].start, self._selection[0].stop, 1)
            self.index_col = np.arange(self._selection[1].start, self._selection[1].stop, 1)

    def swatchMap (self):
        swath = np.random.rand(self.image_area[0], self.image_area[1])
        for col in np.arange(self.image_area[1]):
            swath[:,col] = Sin(col, a1=20, a2=2.0/self.image_area[1])
        return swath

    def spectralCalibrationMap (self):
        """ Generate some type of spectral calibration map to provide a mapping
            from (row,col) to (row,wavelength).
        """
        print ("--> Generating spectral calibration map ...")
        self._scm = np.ndarray(shape=(self.image_area[0], self.image_area[1]))
        for row in range(self.image_area[0]):
            for col in range(self.image_area[1]):
                self._scm[row,col] = 0.01*(col+10*cos(0.5*self.image_area[0]-row))
        return self._scm

    def printSummary (self):
        print "\n[Data] Summary of properties:"
        print "-- Shape signal array .... =", self._lx_data.shape, "->", self._lx_data.size, "pixels"
        print "-- Shape pixel quality ... =", self.pixel_quality.shape
        print "-- Masked pixel data ..... =", self.signal_masked.shape
        print "-- Masked signal selection =", self.signal_selection_masked.shape
        print "-- Selection slices ...... =", self._selection
        print "-- Row selection ......... =", self._selection[0].start, "..", self._selection[0].stop
        print "-- Column selection ...... =", self._selection[1].start, "..", self._selection[1].stop
