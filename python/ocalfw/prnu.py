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
##  Class definition
##
## =============================================================================

class PRNU (object):

    def __init__(self, *args, **kwargs):
        """ Initialize object's internal data.
        """
        # Create data object
        self._data = Data()
        # Detector signal including swath dependent variation
        swath = self._data.swathMap()
        self._data._signal = self._data._signal + swath
        # Pixel quality mask for the full image area (flag pixels with value < 0.1)
        self._data._pixel_quality = np.array(self._data._signal < 0.1, dtype=int)
        # Masked array for the signal array
        self._data.signal_masked = np.ma.masked_array(self._data._signal,
                                                      mask=self._data._pixel_quality)
        self._data.signal_selection_masked = self._data.signal_masked[self._data._selection]

    ##__________________________________________________________________________
    ## Step 1: Remove swath dependent signal variations

    def calc_prnu_step1(self):
        print ("\n[Step 1] Remove swath dependent signal variations\n")

        # Column normalization factor (equation 79a)
        print("--> Computing column normalization factor ...")
        for ncol in range(len(self._data.index_col)):
            self._data.f_norm_col[ncol] = self._data.signal_selection_masked[:, ncol].mean()

        # Row normalization factor (equation 79d)
        print("--> Computing row normalization factor ...")
        for nrow in range(len(self._data.index_row)):
            self._data.f_norm_row[nrow] = np.mean(self._data.signal_selection_masked[nrow, :]/self._data.f_norm_col)

        # Pixel data rown normalization (equation 79e)
        print("--> Pixel data rown normalization ...")
        for nrow in range(len(self._data.index_row)):
            self._data._signal_row_norm[nrow,:] = self._data.signal_masked[nrow, :]/self._data.f_norm_row[nrow]

    ##__________________________________________________________________________

    def calc_prnu_step2(self):
        print ("\n[Step 2] Removal of smile effect\n")

        # Get the spectral map
        print ("--> Get spectral calibration map ...")
        scm = self._data.spectralCalibrationMap()

        # Compute (row,wavelength) mesh points based on spectral map
        print ("--> Computing (row,wavelength) mesh points ...")
        self._data._signal_row_wavelength = np.ndarray(shape=[self._data._signal_row_norm.size,3])

        count = 0
        for nrow in range(len(self._data.index_row)):
            for ncol in range(scm.shape[1]):
                self._data._signal_row_wavelength[count,0] = self._data.index_row[nrow]
                self._data._signal_row_wavelength[count,1] = scm[self._data.index_row[nrow],ncol]
                self._data._signal_row_wavelength[count,2] = self._data._signal_row_norm[nrow,ncol]
                count          += 1

    ##__________________________________________________________________________

    def calc_prnu_step3(self):
        print ("\n[Step 3] Correct for variations in spectral intensity\n")

    ##__________________________________________________________________________

    def calc_prnu_step4(self):
        print ("\n[Step 4] Removal of high-frequency features\n")

    ##__________________________________________________________________________

    def calc_prnu_step5(self):
        print ("\n[Step 5] Re-introduction of high-frequency variations\n")

    ##__________________________________________________________________________

    def calc_prnu_step6(self):
        print ("\n[Step 6] Re-gridding to Detector grid\n")

    ##__________________________________________________________________________

    def calc_prnu_step7(self):
        print ("\n[Step 7] Inverse normalization of row intensities\n")

        # Temporary data
        signal_norm_row_smooth = np.ones(shape=self._data._signal_row_norm.shape)

        # Apply normalization factor
        for nrow in range(len(self._data.index_row)):
            self._data._signal_smooth[nrow,:] = signal_norm_row_smooth[nrow, :]*self._data.f_norm_row[nrow]

    ##__________________________________________________________________________

    def calc_prnu_step8(self):
        print ("\n[Step 8] Calculate PRNU CKD\n")

    ##__________________________________________________________________________

    def calc_prnu(self):
        """ Calculate PRNU CKD.
        """
        self.calc_prnu_step1()
        self.calc_prnu_step2()
        self.calc_prnu_step3()
        self.calc_prnu_step4()
        self.calc_prnu_step5()
        self.calc_prnu_step6()
        self.calc_prnu_step7()
        self.calc_prnu_step8()

    ##__________________________________________________________________________

    def report_prnu(self):
        """ Generate plots for reporting.
        """
        print ("\n[Reporting]\n")
        report = ReportPRNU()
        report.step1(self._data)
        report.step2(self._data)
        report.step3(self._data)
        report.step4(self._data)
        report.step5(self._data)
        report.step6(self._data)
        report.step7(self._data)
        report.step8(self._data)

    ##__________________________________________________________________________

    def run(self):
        self.calc_prnu()
        self.report_prnu()

