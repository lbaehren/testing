import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pylab import *

## =============================================================================
##
##  Data containers
##
## =============================================================================

##______________________________________________________________________________
##                                                                          Data

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
        self._scm = np.ndarray(shape=(self.image_area[0], self.image_area[1]))
        for col in range(self.image_area[1]):
            self._scm[:,col] = 0.01*col
        return self._scm

    def printSummary (self):
        print "\n[Data] Summary of properties:"
        print "-- Shape signal array .... =", self._lx_data.shape, "->", self._lx_data.size, "pixels"
        print "-- Shape pixel quality ... =", self.pixel_quality.shape
        print "-- Masked pixel data ..... =", signal_masked.shape
        print "-- Masked signal selection =", signal_selection_masked.shape
        print "-- Selection slices ...... =", self._selection
        print "-- Row selection ......... =", self._selection[0].start, "..", self._selection[0].stop
        print "-- Column selection ...... =", self._selection[1].start, "..", self._selection[1].stop

## =============================================================================
##
##  Helper functions
##
## =============================================================================

##______________________________________________________________________________
##                                                                           Sin

def Sin (x,
         a0=0.0,
         a1=1.0,
         a2=1.0,
         a3=0.0):
    """ Generalized sin function, including offsets and scale factors.
    """
    return a0+a1*np.sin(a2*x+a3)

##______________________________________________________________________________
##                                                                    plot_image

def plot_image (imageData,
                xlabel="Row number",
                ylabel="Column number"):
    plt.imshow(imageData)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


##______________________________________________________________________________
##                                                                   plots_step1

def plots_step1 (data):
    """ Generate diagnostics plots for PRNU step 1.
    """
    print("--> Generating diagnostics plots ...")
    ## Plot detector signal for the selected region
    plot_image(data._lx_data[data._selection])
    ## Plot row normalization factor
    plt.plot(data.index_row, data.f_norm_row, '-')
    plt.xlabel("Row number")
    plt.ylabel("Row normalization factor")
    plt.show()
    ## Plot column normalization factor
    plt.plot(data.index_col, data.f_norm_col, '-')
    plt.xlabel("Column number")
    plt.ylabel("Column normalization factor")
    plt.show()

##______________________________________________________________________________
##                                                                   plots_step2

def plots_step2 (data):
    """ Generate diagnostics plots for PRNU step 2.
    """
    print("--> Generating diagnostics plots ...")

##______________________________________________________________________________
##                                                                   plots_step3

def plots_step3 (data):
    """ Generate diagnostics plots for PRNU step 3.
    """
    print("--> Generating diagnostics plots ...")

## =============================================================================
##
## Preparation of data
##
## =============================================================================

## Create data object
data = Data()

## Detector signal including swatch dependent variation

swath = data.swatchMap()
data._lx_data = data._lx_data + swath

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
data.pixel_quality = np.array(data._lx_data < 0.1, dtype=int)

## Masked array for the signal array
signal_masked = np.ma.masked_array(data._lx_data, mask=data.pixel_quality)
signal_selection_masked = signal_masked[data._selection]

##______________________________________________________________________________
## Print summary

data.printSummary()


## =============================================================================
##
##  PRNU CKD calculation
##
## =============================================================================

##______________________________________________________________________________
## Step 1: Remove swath dependent signal variations

print "\n[Step 1]\n"

## Column normalization factor (equation 79a)

print("--> Computing column normalization factor ...")

for ncol in range(len(data.index_col)):
    data.f_norm_col[ncol] = signal_selection_masked[:, ncol].mean()

## Row normalization factor (equation 79d)

print("--> Computing row normalization factor ...")

for nrow in range(len(data.index_row)):
    data.f_norm_row[nrow] = np.mean(signal_selection_masked[nrow, :]/data.f_norm_col)

## Pixel data rown normalization (equation 79e)

print("--> Pixel data rown normalization ...")

signal_row_norm = np.ndarray(shape=(len(data.index_row),data.image_area[1]), dtype=float)

for nrow in range(len(data.index_row)):
    signal_row_norm[nrow,:] = signal_masked[nrow, :]/data.f_norm_row[nrow]
    
plot_image(signal_row_norm)

plots_step1(data)

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2]\n"

## Get the spectral map
scm = data.spectralCalibrationMap()

plot_image(scm)

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

print "\n[Step 3]\n"

##______________________________________________________________________________
## Step 4 : Removal of high-frequency features

print "\n[Step 4]\n"

##______________________________________________________________________________
## Step 5 : Re-introduction of high-frequency variations

##______________________________________________________________________________
## Step 6 : Re-gridding to Detector grid

##______________________________________________________________________________
## Step 7 : Inverse normalization of row intensities

##______________________________________________________________________________
## Step 8 : Calculate PRNU CKD
