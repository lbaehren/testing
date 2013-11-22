import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pylab import *
from data import Data
from report_prnu import ReportPRNU
import filters

## =============================================================================
##
## Preparation of data
##
## =============================================================================

## Create data object
data = Data()

## Detector signal including swath dependent variation

swath = data.swathMap()
data._signal = data._signal + swath

## Pixel quality mask for the full image area (flag pixels with value < 0.1)
data._pixel_quality = np.array(data._signal < 0.1, dtype=int)

## Masked array for the signal array
data.signal_masked = np.ma.masked_array(data._signal, mask=data._pixel_quality)
data.signal_selection_masked = data.signal_masked[data._selection]

##______________________________________________________________________________
## Print summary

data.printSummary()


## =============================================================================
##
##  PRNU CKD calculation
##
## =============================================================================

report = ReportPRNU()

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

## Summary of data array
print "--> Summary of data arrays:"
print " - data._signal ........ :", data._signal.shape
print " - data.f_norm_col ..... :", data.f_norm_col.shape
print " - data.f_norm_row ..... :", data.f_norm_row.shape
print " - data._signal_row_norm :", data._signal_row_norm.shape

report.step1(data)

##______________________________________________________________________________
## Step 2: Removal of smile effect by re-gridding the columns to wavelength grid

print "\n[Step 2] Removal of smile effect\n"

## Get the spectral map
scm = data.spectralCalibrationMap()

# Compute (row,wavelength) mesh points based on spectral map
data._signal_row_wavelength = np.ndarray(shape=[data._signal_row_norm.size,3])

print ("--> Computing (row,wavelength) mesh points ...")
print " - smc ................. =", scm.shape
print " - data._signal_row_norm =", data._signal_row_norm.shape
print " - data.index_row ...... =", min(data.index_row), "...", max(data.index_row)
count = 0
for nrow in range(len(data.index_row)):
    for ncol in range(scm.shape[1]):
        data._signal_row_wavelength[count,0] = data.index_row[nrow]
        data._signal_row_wavelength[count,1] = scm[data.index_row[nrow],ncol]
        data._signal_row_wavelength[count,2] = data._signal_row_norm[nrow,ncol]
        count          += 1

report.step2(data)

##______________________________________________________________________________
## Step 3: Correct for variations in spectral intensity

print "\n[Step 3] Correct for variations in spectral intensity\n"

report.step3(data)

##______________________________________________________________________________
## Step 4 : Removal of high-frequency features

print "\n[Step 4] Removal of high-frequency features\n"

report.step4(data)

##______________________________________________________________________________
## Step 5 : Re-introduction of high-frequency variations

print "\n[Step 5] Re-introduction of high-frequency variations\n"

report.step5(data)

##______________________________________________________________________________
## Step 6 : Re-gridding to Detector grid

print "\n[Step 6] Re-gridding to Detector grid\n"

report.step6(data)

##______________________________________________________________________________
## Step 7 : Inverse normalization of row intensities

print "\n[Step 7] Inverse normalization of row intensities\n"

signal_norm_row_smooth = np.ones(shape=data._signal_row_norm.shape)

for nrow in range(len(data.index_row)):
    data._signal_smooth[nrow,:] = signal_norm_row_smooth[nrow, :]*data.f_norm_row[nrow]

report.step7(data)

##______________________________________________________________________________
## Step 8 : Calculate PRNU CKD

print "\n[Step 8] Calculate PRNU CKD\n"

report.step8(data)
