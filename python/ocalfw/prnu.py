import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pylab import *
from data import Data
import filters

## =============================================================================
##
##  Diagnostics plots
##
## =============================================================================

##______________________________________________________________________________
##                                                                   plots_step1

def plots_step1 (data,
                 outfile='plots_prnu_step1.pdf'):
    """ Generate diagnostics plots for PRNU step 1.
    """
    print("--> Generating diagnostics plots ...")

    ## Create new PDF document
    pdf_pages = PdfPages(outfile)

    ## Detector signal for full CCD
    fig = plt.figure ()
    plt.imshow(data._lx_data)
    plt.title("Detector signal for full CCD")
    plt.xlabel("Column number")
    plt.ylabel("Row number")
    pdf_pages.savefig(fig)
    plt.close()

    ## Histogram of detector signal for full CCD
    fig = plt.figure ()
    plt.hist(data._lx_data.flatten(), bins=100, facecolor='g', normed=1)
    plt.title("Distribution of detector signal values")
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

    ## Row normalized detector signal
    fig = plt.figure ()
    plt.imshow(data._signal_row_norm)
    plt.title("Row normalized detector signal")
    plt.xlabel("Column number")
    plt.ylabel("Row number")
    pdf_pages.savefig(fig)
    plt.close()

    ## Histogram for row normalized detector signal
    fig = plt.figure ()
    plt.hist(data._signal_row_norm.flatten(), bins=100, facecolor='g', normed=1)
    plt.title("Distribution of row normalized detector signal")
    pdf_pages.savefig(fig)
    plt.close()

    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step2

def plots_step2 (data,
                 outfile='plots_prnu_step2.pdf'):
    """ Generate diagnostics plots for PRNU step 2.
    """
    print("--> Generating diagnostics plots ...")

    ## Create new PDF document
    pdf_pages = PdfPages(outfile)

    ## Plot spectral calibration map
    fig = plt.figure ()
    plt.imshow(data._scm)
    plt.title("Spectral calibration map")
    plt.xlabel("Column number")
    plt.ylabel("Row number")
    pdf_pages.savefig(fig)
    plt.close()

    ## Cross-sections through spectral calibration map
    fig = plt.figure ()
    plt.plot(data._scm[200,:])
    plt.plot(data._scm[400,:])
    plt.plot(data._scm[600,:])
    plt.plot(data._scm[800,:])
    plt.title("Spectral calibration map cross-sections")
    plt.xlabel("Column number")
    plt.ylabel("Wavelength")
    pdf_pages.savefig(fig)
    plt.close()

    ## Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step3

def plots_step3 (data,
                 outfile='plots_prnu_step3.pdf'):
    """ Generate diagnostics plots for PRNU step 3.
    """
    print("--> Generating diagnostics plots ...")
    # Create new PDF document
    pdf_pages = PdfPages(outfile)
    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step4

def plots_step4 (data,
                 outfile='plots_prnu_step4.pdf'):
    """ Generate diagnostics plots for PRNU step 4.
    """
    print("--> Generating diagnostics plots ...")

    # Create new PDF document
    pdf_pages = PdfPages(outfile)

    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step5

def plots_step5 (data,
                 outfile='plots_prnu_step5.pdf'):
    """ Generate diagnostics plots for PRNU step 5.
    """
    print("--> Generating diagnostics plots ...")

    # Create new PDF document
    pdf_pages = PdfPages(outfile)

    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step6

def plots_step6 (data,
                 outfile='plots_prnu_step6.pdf'):
    """ Generate diagnostics plots for PRNU step 6.
    """
    print("--> Generating diagnostics plots ...")

    # Create new PDF document
    pdf_pages = PdfPages(outfile)

    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step7

def plots_step7 (data,
                 outfile='plots_prnu_step7.pdf'):
    """ Generate diagnostics plots for PRNU step 7.
    """
    print("--> Generating diagnostics plots ...")

    # Create new PDF document
    pdf_pages = PdfPages(outfile)

    ## Smoothed signal after removal of high-frequency features
    fig = plt.figure ()
    plt.imshow(data._signal_smooth)
    plt.title("Smoothed signal after removal of high-frequency features")
    plt.xlabel("Column number")
    plt.ylabel("Row number")
    pdf_pages.savefig(fig)
    plt.close()

    # Write the PDF document to the disk
    pdf_pages.close()

##______________________________________________________________________________
##                                                                   plots_step8

def plots_step8 (data,
                 outfile='plots_prnu_step8.pdf'):
    """ Generate diagnostics plots for PRNU step 8.
    """
    print("--> Generating diagnostics plots ...")

    # Create new PDF document
    pdf_pages = PdfPages(outfile)

    # Write the PDF document to the disk
    pdf_pages.close()

## =============================================================================
##
## Preparation of data
##
## =============================================================================

## Create data object
data = Data()

## Detector signal including swath dependent variation

swath = data.swathMap()
data._lx_data = data._lx_data + swath

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

print "\n[Step 1] Remove swath dependent signal variations\n"

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

for nrow in range(len(data.index_row)):
    data._signal_row_norm[nrow,:] = data.signal_masked[nrow, :]/data.f_norm_row[nrow]
    
plots_step1(data)

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2] Removal of smile effect\n"

## Get the spectral map
scm = data.spectralCalibrationMap()

plots_step2(data)

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

print "\n[Step 3] Correct for variations in spectral intensity\n"

plots_step3(data)

##______________________________________________________________________________
## Step 4 : Removal of high-frequency features

print "\n[Step 4] Removal of high-frequency features\n"

plots_step4(data)

##______________________________________________________________________________
## Step 5 : Re-introduction of high-frequency variations

print "\n[Step 5] Re-introduction of high-frequency variations\n"

plots_step5(data)

##______________________________________________________________________________
## Step 6 : Re-gridding to Detector grid

print "\n[Step 6] Re-gridding to Detector grid\n"

plots_step6(data)

##______________________________________________________________________________
## Step 7 : Inverse normalization of row intensities

print "\n[Step 7] Inverse normalization of row intensities\n"

signal_norm_row_smooth = np.ones(shape=data._signal_row_norm.shape)

for nrow in range(len(data.index_row)):
    data._signal_smooth[nrow,:] = signal_norm_row_smooth[nrow, :]*data.f_norm_row[nrow]

plots_step7(data)

##______________________________________________________________________________
## Step 8 : Calculate PRNU CKD

print "\n[Step 8] Calculate PRNU CKD\n"

plots_step8(data)
