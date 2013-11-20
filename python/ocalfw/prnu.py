import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pylab import *
from data import Data
from filters import Hanning2D

## =============================================================================
##
##  Helper functions
##
## =============================================================================

##______________________________________________________________________________
##                                                                     image2pdf

def image2pdf(imageData,
              outfile,
              title="Detector image",
              xlabel="Column number",
              ylabel="Row number"):
    """ Plot image data to PDF. """
    plt.imshow(imageData)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(outfile)
    plt.close()

## =============================================================================
##
##  Diagnostics plots
##
## =============================================================================

##______________________________________________________________________________
##                                                                   plots_step1

def plots_step1 (data):
    """ Generate diagnostics plots for PRNU step 1.
    """
    print("--> Generating diagnostics plots ...")
    pdf_pages = PdfPages('plots_prnu_step1.pdf')
    ## Plot row normalization factor
    fig = plt.figure ()
    plt.plot(data.index_row, data.f_norm_row, '-')
    plt.title("Row normalization factor")
    plt.xlabel("Row number")
    plt.ylabel("Row normalization factor")
    pdf_pages.savefig(fig)
    plt.close()
    ## Plot column normalization factor
    fig = plt.figure ()
    plt.plot(data.index_col, data.f_norm_col, '-')
    plt.title("Column normalization factor")
    plt.xlabel("Column number")
    plt.ylabel("Column normalization factor")
    pdf_pages.savefig(fig)
    plt.close()
    ## Plot detector signal for the selected region
    fig = plt.figure ()
    plt.imshow(data._lx_data[data._selection])
    plt.title("Detector signal selection")
    plt.xlabel("Column number")
    plt.ylabel("Row number")
    pdf_pages.savefig(fig)
    plt.close()
    # Write the PDF document to the disk
    pdf_pages.close()

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

## Detector signal including swath dependent variation

swath = data.swatchMap()
data._lx_data = data._lx_data + swath

image2pdf(swath, "plot_swath.pdf", "Swath dependent variation")

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
data.pixel_quality = np.array(data._lx_data < 0.1, dtype=int)

## Masked array for the signal array
data.signal_masked = np.ma.masked_array(data._lx_data, mask=data.pixel_quality)
data.signal_selection_masked = data.signal_masked[data._selection]

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
    data.f_norm_col[ncol] = data.signal_selection_masked[:, ncol].mean()

## Row normalization factor (equation 79d)

print("--> Computing row normalization factor ...")

for nrow in range(len(data.index_row)):
    data.f_norm_row[nrow] = np.mean(data.signal_selection_masked[nrow, :]/data.f_norm_col)

## Pixel data rown normalization (equation 79e)

print("--> Pixel data rown normalization ...")

signal_row_norm = np.ndarray(shape=(len(data.index_row),data.image_area[1]), dtype=float)

for nrow in range(len(data.index_row)):
    signal_row_norm[nrow,:] = data.signal_masked[nrow, :]/data.f_norm_row[nrow]
    
plots_step1(data)

image2pdf(signal_row_norm, "plot_signal_row_norm.pdf", "Row normalized detector signal")

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2]\n"

## Get the spectral map
scm = data.spectralCalibrationMap()

image2pdf(scm, "plot_scm.pdf", "Spectral calibration map")

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

print "\n[Step 3]\n"

## 2D Hanning window
hanning_row = np.hanning(len(data.index_row))
hanning_col = np.hanning(len(data.index_col))
hanning2d   = np.ndarray(shape=(len(data.index_row),len(data.index_col)))

for nrow in range(len(data.index_row)):
    hanning2d[nrow,:] = hanning_col

for ncol in range(len(data.index_col)):
    hanning2d[:,ncol] = hanning2d[:,ncol]*hanning_row

print "2D Hanning window:"
print "-- Shape ......... =", hanning2d.shape
print "-- nof. elements . =", hanning2d.size
print "-- Sum of elements =", np.sum(hanning2d)

image2pdf(hanning2d, "plot_hanning2d.pdf",title="2D Hanning window")

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
