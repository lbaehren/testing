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
        self.image_area = []  ## Image area for full CCD
        self.selection  = []  ## Image area selection slices
        self.lx_data    = []  ## Detector signal for full CCD
        self.f_norm_row = []  ## Row normalization factor
        self.f_norm_col = []  ## Column normalization factor
        self.index_row  = []  ## Row number index for selection
        self.index_col  = []  ## Column number index for selection
        self.csm        = []  ## Spectral calibration map

    def setSelection (selection):
        """ Set image area selection.
        """
        if len(selection)==2:
            self.selection = selection
            self.f_norm_row = np.zeros(self.selection[0].stop-self.selection[0].start, 'float32')
            self.f_norm_col = np.zeros(self.selection[1].stop-self.selection[1].start, 'float32')
            self.index_row = np.arange(self.selection[0].start, self.selection[0].stop, 1)
            self.index_col = np.arange(self.selection[1].start, self.selection[1].stop, 1)

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
data.image_area = (1024,600)
data.selection  = [ slice(100,500), slice(200,500) ]

## Detector signal including swatch dependent variation
data.lx_data = np.random.rand(data.image_area[0],data.image_area[1])
swath  = np.random.rand(data.image_area[0],data.image_area[1])

for col in np.arange(data.image_area[1]):
    swath[:,col] = generalized_sin(col, a1=20, a2=2.0/data.image_area[1])

data.lx_data = data.lx_data + swath

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
pixel_quality = np.array(data.lx_data < 0.1, dtype=int)

## Masked array for the signal array
signal_masked = np.ma.masked_array(data.lx_data, mask=pixel_quality)
signal_selection_masked = signal_masked[data.selection]

##______________________________________________________________________________
## Print summary

print "\n[Input data] Summary:\n"

print "-- Shape signal array .... =", data.lx_data.shape, "->", data.lx_data.size, "pixels"
print "-- Shape pixel quality ... =", pixel_quality.shape
print "-- Masked pixel data ..... =",signal_masked.shape
print "-- Masked signal selection =", signal_selection_masked.shape
print "-- Selection slices ...... =", data.selection
print "-- Row selection ......... =", data.selection[0].start, "..", data.selection[0].stop
print "-- Column selection ...... =", data.selection[1].start, "..", data.selection[1].stop

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

print("--> Allocating normalization arrays...")
data.f_norm_row = np.zeros(data.selection[0].stop-data.selection[0].start, 'float32')
data.f_norm_col = np.zeros(data.selection[1].stop-data.selection[1].start, 'float32')

data.index_row = np.arange(data.selection[0].start, data.selection[0].stop, 1)
data.index_col = np.arange(data.selection[1].start, data.selection[1].stop, 1)

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

