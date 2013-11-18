import numpy as np
import matplotlib.pyplot as plt
from pylab import *

## =============================================================================
##
##  Function definitions
##
## =============================================================================

def my_sin (x,
            a0=0.0,
            a1=1.0,
            a2=1.0,
            a3=0.0):
    """ Generalized sin function, including offsets and scale factors.
    """
    return a0+a1*np.sin(a2*x+a3)

def plot_grid ():
    """ Display coordinate grid.
    """
    axes = gca()
    axes.set_xlim(0,4)
    axes.set_ylim(0,3)
    axes.set_xticklabels([])
    axes.set_yticklabels([])

    show()

def spectral_map (image_shape):
    """ Map for the mapping from detector pixel coordinates (row,col) to
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
image_area = (1024,600)
selection  = [ slice(100,500), slice(100,200) ]

## Detector signal including swatch dependent variation
signal = np.random.rand(image_area[0],image_area[1])
swath  = np.random.rand(image_area[0],image_area[1])

for col in np.arange(image_area[1]):
    swath[:,col] = my_sin(col, a1=20, a2=2.5/image_area[1])

signal = signal + swath

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
pixel_quality = np.array(signal < 0.1, dtype=int)

##______________________________________________________________________________
## Print summary

print "-- Shape signal array =", signal.shape, "->", signal.size, "pixels"
print "-- Shape mask array   =", pixel_quality.shape
print "-- Selection slices   =", selection

##______________________________________________________________________________
## Plot generated input data

plt.imshow(signal)
plt.show()

## =============================================================================
##
##  PRNU CKD calculation
##
## =============================================================================

##______________________________________________________________________________
## Step 1: Remove swath dependent signal variations

print "\n[Step 1]\n"

print("--> Allocating normalization arrays...")
f_norm_row = np.array(selection[0].stop-selection[0].start, 'float32')
f_norm_col = np.array(selection[1].stop-selection[1].start, 'float32')

## Column normalization factor (equation 79a)
print("--> Computing column normalization factor ...")
for ncol in range(selection[1].start, selection[1].stop):
    print "Processing column",ncol,ncol-selection[1].start
    f_norm_col[ncol-selection[1].start] = signal_selection_masked[:, ncol].mean()

## Row normalization factor (equation 79d)
print("--> Computing row normalization factor ...")
for nrow in range(selection[0].start, selection[0].stop):
    print "... processing row", nrow
    f_norm_row[nrow-selection[0].start] = np.mean(signal_selection_masked[nrow, :]/f_norm_col)


## Plot data and normalization values

xvals = np.arange(selection[0].start, selection[0].stop, 1)
yvals = np.arange(selection[1].start, selection[1].stop, 1)

plt.plot(yvals, f_norm_col, '+-')
plt.show()

plt.imshow(signal_selection)
plt.show()

## Print summary for this step
print "[Step 1] Summary:"
print "-- signal_selection_masked =", signal_selection_masked.shape
print "-- f_norm_row shape ...... =", f_norm_row.shape
print "-- f_norm_col shape ...... =", f_norm_col.shape
print "-- xvals ................. =", np.min(xvals), "..", np.max(xvals)
print "-- yvals ................. =", np.min(yvals), "..", np.max(yvals)

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2]\n"

## Get the spectral map
spectralimage_map = spectral_map(image_area)

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

