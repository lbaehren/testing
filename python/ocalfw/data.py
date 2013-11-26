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

def Circle (x,
            y,
            x0=0.0,
            y0=0.0,
            a0=1.0,
            a1=1.0,
            a2=1.0):
    """ General definition of circle, or rather an ellipse.
    """
    r = a0 * np.sqrt(a1*(x-x0)**2 + a2*(y-y0)**2)
    return r

## =============================================================================
##
##  Class definition
##
## =============================================================================

class Data(object):
    """ Data object to facilitate passing around input and generated data.
    """

    ##__________________________________________________________________________
    ##                                                                  __init__

    def __init__(self, *args, **kwargs):
        """ Initialize object's internal data.
        """

        """Image area for full CCD. """
        self.image_area = (1024,600)
        """ Image area selection slices. """
        self._selection = [ slice(100,500), slice(200,500) ]
        """ Swath angle dependent signal variation. """
        self._swath = np.random.rand(self.image_area[0], self.image_area[1])
        """ Spectral calibration map (SCM). """
        self._scm = []
        """ (row,wavelength) mesh points derived from spectral calibration map. """
        self._signal_row_wavelength = []
        """ Detector signal for full CCD. """
        self._signal = np.random.rand(self.image_area[0],self.image_area[1])
        """ Pixel quality mask for full CCD. """
        self._pixel_quality = []
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
        """ Smoothed signal after removal of high-frequency features. """
        self._signal_smooth = np.ndarray(shape=self._signal_row_norm.shape, dtype=float)
        """ Normalization factor for spectral intensity. """
        self._f_norm_wavelength = np.ones([self.image_area[1]])
        """ PRNU map. """
        self._prnu = np.random.rand(self._signal_row_norm.shape[0],self._signal_row_norm.shape[1])

    ##__________________________________________________________________________
    ##                                                              setSelection

    def setSelection (self, selection):
        """ Set image area selection.
        """
        if len(selection)==2:
            self._selection = selection
            self.f_norm_row = np.zeros(self._selection[0].stop-self._selection[0].start, 'float32')
            self.f_norm_col = np.zeros(self._selection[1].stop-self._selection[1].start, 'float32')
            self.index_row  = np.arange(self._selection[0].start, self._selection[0].stop, 1)
            self.index_col  = np.arange(self._selection[1].start, self._selection[1].stop, 1)

    ##__________________________________________________________________________
    ##                                                                  swathMap

    def swathMap (self):
        """ Generate map of swath dependent signal variation. """
        for col in np.arange(self.image_area[1]):
            self._swath[:,col] = Sin(col, a1=20, a2=2.0/self.image_area[1])
        return self._swath

    ##__________________________________________________________________________
    ##                                                    spectralCalibrationMap

    def spectralCalibrationMap (self):
        """ Generate some type of spectral calibration map to provide a mapping
            from (row,col) to (row,wavelength).
        """
        self._scm = np.ndarray(shape=(self.image_area[0], self.image_area[1]))
        for row in range(self.image_area[0]):
            rowValue = 0.5*self.image_area[0]-row
            for col in range(self.image_area[1]):
                self._scm[row,col] = Circle(rowValue,2*col, y0=0.5*col, a0=10)
        return self._scm

    ##__________________________________________________________________________
    ##                                                              printSummary

    def printSummary (self):
        print "\n[Data] Summary of properties:"
        print "-- Shape signal array .... =", self._signal.shape, "->", self._signal.size, "pixels"
        print "-- Shape pixel quality ... =", self._pixel_quality.shape
        print "-- Masked pixel data ..... =", self.signal_masked.shape
        print "-- Masked signal selection =", self.signal_selection_masked.shape
        print "-- Selection slices ...... =", self._selection
        print "-- Row selection ......... =", self._selection[0].start, "..", self._selection[0].stop
        print "-- Column selection ...... =", self._selection[1].start, "..", self._selection[1].stop
