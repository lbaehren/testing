import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## =============================================================================
##
##  Data containers
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
        self.selection = [ slice(100,500), slice(200,500) ]
        """ Detector signal for full CCD. """
        self.lx_data = np.random.rand(self.image_area[0],self.image_area[1])
        """ Pixel quality mask for full CCD. """
        self.pixel_quality = []
        """ Row normalization factor. """
        self.f_norm_row = np.zeros(self.selection[0].stop-self.selection[0].start, 'float32')
        """ Column normalization factor. """
        self.f_norm_col = np.zeros(self.selection[1].stop-self.selection[1].start, 'float32')
        """ Row number index for selection. """
        self.index_row = np.arange(self.selection[0].start, self.selection[0].stop, 1)
        """ Column number index for selection. """
        self.index_col = np.arange(self.selection[1].start, self.selection[1].stop, 1)
        """ Spectral calibration map. """
        self.csm = []

    def setSelection (selection):
        """ Set image area selection.
        """
        if len(selection)==2:
            self.selection = selection
            self.f_norm_row = np.zeros(self.selection[0].stop-self.selection[0].start, 'float32')
            self.f_norm_col = np.zeros(self.selection[1].stop-self.selection[1].start, 'float32')
            self.index_row = np.arange(self.selection[0].start, self.selection[0].stop, 1)
            self.index_col = np.arange(self.selection[1].start, self.selection[1].stop, 1)

    def printSummary (self):
        print "\n[Data] Summary of properties:"
        print "-- Shape signal array .... =", self.lx_data.shape, "->", self.lx_data.size, "pixels"
        print "-- Shape pixel quality ... =", self.pixel_quality.shape
        print "-- Masked pixel data ..... =",signal_masked.shape
        print "-- Masked signal selection =", signal_selection_masked.shape
        print "-- Selection slices ...... =", self.selection
        print "-- Row selection ......... =", self.selection[0].start, "..", self.selection[0].stop
        print "-- Column selection ...... =", self.selection[1].start, "..", self.selection[1].stop

## =============================================================================
##
##  Helper functions
##
## =============================================================================

##______________________________________________________________________________
##                                                               generalized_sin

def generalized_sin (x,
                     a0=0.0,
                     a1=1.0,
                     a2=1.0,
                     a3=0.0):
    """ Generalized sin function, including offsets and scale factors.
    """
    return a0+a1*np.sin(a2*x+a3)

##______________________________________________________________________________
##                                                                   plots_step1

def plots_step1 (data):
    """ Generate diagnostics plots for PRNU step 1.
    """
    print("--> Generating diagnostics plots ...")
    ## Plot detector signal for the selected region
    plt.imshow(data.lx_data[data.selection])
    plt.show()
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

##______________________________________________________________________________
##                                                      spectral_calibration_map

def spectral_calibration_map (image_shape):
    """ Spectral calibration map detector pixel coordinates (row,col) to
        wavelength coordinates.
    """
    print "[spectral_map] Function not yet implemented!"
    print "-- Image shape = ", image_shape

## =============================================================================
##
## Preparation of data
##
## =============================================================================

## Definition of areas  (row,col)
data = Data()

## Detector signal including swatch dependent variation
swath = np.random.rand(data.image_area[0],data.image_area[1])

for col in np.arange(data.image_area[1]):
    swath[:,col] = generalized_sin(col, a1=20, a2=2.0/data.image_area[1])

data.lx_data = data.lx_data + swath

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
data.pixel_quality = np.array(data.lx_data < 0.1, dtype=int)

## Masked array for the signal array
signal_masked = np.ma.masked_array(data.lx_data, mask=data.pixel_quality)
signal_selection_masked = signal_masked[data.selection]

##______________________________________________________________________________
## Print summary

data.printSummary()

##______________________________________________________________________________
## Plot generated input data

#plt.imshow(signal)
#plt.show()

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
    
plt.imshow(signal_row_norm)
plt.show()

plots_step1(data)

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2]\n"

## Get the spectral map
spectralimage_map = spectral_calibration_map(data.image_area)

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

