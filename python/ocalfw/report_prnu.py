""" Reporting for the PRNU algorithm: generation of diagnostic plots for each
    of the individual processing steps to inspect the performance and accuracy.
"""

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from data import Data

## =============================================================================
##
##  Class definition
##
## =============================================================================

class ReportPRNU (object):

    def __init__(self, *args, **kwargs):
        """ Initialize object's internal data.
        """

        """ Enable/displable generation of 3D plots. """
        self._with3D = False
        """ Enable/displable generation of scatter plots. """
        self._withScatter = True

    ##__________________________________________________________________________
    ##                                                                     step1

    def step1 (self,
               data,
               outfile='plots_prnu_step1.pdf'):
        """ Generate diagnostics plots for PRNU step 1.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 1 ...")

        ## Create new PDF document
        pdf_pages = PdfPages(outfile)

        ## Detector signal for full CCD
        fig = plt.figure ()
        plt.imshow(data._signal)
        plt.title("Detector signal for full CCD")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        ## Histogram of detector signal for full CCD
        fig = plt.figure ()
        plt.hist(data._signal.flatten(), bins=100, facecolor='g', normed=1)
        plt.title("Distribution of detector signal values")
        pdf_pages.savefig(fig)
        plt.close()

        ## Plot detector signal for the selected region
        fig = plt.figure ()
        plt.imshow(data._signal[data._selection])
        plt.title("Detector signal selection")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
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
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        ## Histogram for row normalized detector signal
        fig = plt.figure ()
        plt.hist(data._signal_row_norm.flatten(), bins=100, facecolor='g', normed=1)
        plt.title("Distribution of row normalized detector signal")
        pdf_pages.savefig(fig)
        plt.close()

        # Difference between input detector signal and row normalized detector signal
        diff_signal = np.ndarray(shape=data._signal_row_norm.shape)
        for nrow in range(len(data.index_row)):
            diff_signal[nrow, :] = data._signal[data.index_row[nrow], :]-data._signal_row_norm[nrow, :]
        fig = plt.figure ()
        plt.imshow(diff_signal)
        plt.title("Difference between input and row norm. signal")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        # Histogram for difference between input detector signal and row normalized detector signal
        fig = plt.figure ()
        plt.hist(diff_signal.flatten(), bins=100, facecolor='b', normed=1)
        plt.title("Difference between input detector signal and row normalized detector signal")
        pdf_pages.savefig(fig)
        plt.close()

        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step2

    def step2 (self,
               data,
               outfile='plots_prnu_step2.pdf'):
        """ Generate diagnostics plots for PRNU step 2.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 2 ...")

        ## Create new PDF document
        pdf_pages = PdfPages(outfile)

        ## Plot spectral calibration map
        fig = plt.figure ()
        plt.imshow(data._scm)
        plt.title("Spectral calibration map")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        ## Plot (row,wavelength) mesh points derived from spectral calibration map
        if (self._withScatter):
            fig = plt.figure ()
            plt.scatter(data._signal_row_wavelength[:,1],
                        data._signal_row_wavelength[:,0],
                        marker='x',
                        c='g',
                        s=2)
            plt.xlabel("Wavelength (x)")
            plt.ylabel("Row (y)")
            plt.title("Scatter plot of (row,wavelength) mesh grid")
            pdf_pages.savefig(fig)
            plt.close()

        ## Plot detector signal as represented on an irregular (row,wavelength) mesh grid
        if (self._withScatter):
            fig = plt.figure()
            ax  = fig.gca(projection='3d')
            cmhot = plt.cm.get_cmap("hot")
            ax.scatter(data._signal_row_wavelength[:,1],
                       data._signal_row_wavelength[:,0],
                       data._signal_row_wavelength[:,2],
                       c=data._signal_row_wavelength[:,2],
                       cmap=cmhot)
            plt.xlabel("Wavelength (x)")
            plt.ylabel("Row (y)")
            plt.title("Signal as function of (row,wavelength)")
            pdf_pages.savefig(fig)
            plt.close()

        ## Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step3

    def step3 (self,
               data,
               outfile='plots_prnu_step3.pdf'):
        """ Generate diagnostics plots for PRNU step 3.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 3 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)

        ## Plot row normalization factor
        fig = plt.figure ()
        plt.plot(data._f_norm_wavelength, '-')
        plt.title("Normalization factor for spectral intensity")
        plt.xlabel("Row number")
        plt.ylabel("Normalization factor")
        pdf_pages.savefig(fig)
        plt.close()

        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step4

    def step4 (self,
               data,
               outfile='plots_prnu_step4.pdf'):
        """ Generate diagnostics plots for PRNU step 4.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 4 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)
        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step5

    def step5 (self,
               data,
               outfile='plots_prnu_step5.pdf'):
        """ Generate diagnostics plots for PRNU step 5.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 5 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)
        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step6

    def step6 (self,
               data,
               outfile='plots_prnu_step6.pdf'):
        """ Generate diagnostics plots for PRNU step 6.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 6 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)
        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step7

    def step7 (self,
               data,
               outfile='plots_prnu_step7.pdf'):
        """ Generate diagnostics plots for PRNU step 7.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 7 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)

        # Smoothed signal after removal of high-frequency features
        fig = plt.figure ()
        plt.imshow(data._signal_smooth)
        plt.title("Smoothed signal after removal of high-frequency features")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        # Write the PDF document to the disk
        pdf_pages.close()

    ##__________________________________________________________________________
    ##                                                                     step8

    def step8 (self,
               data,
               outfile='plots_prnu_step8.pdf'):
        """ Generate diagnostics plots for PRNU step 8.

            :param data: Data object with (temporary) data from the PRNU CKD
                  calculation algorithm."
            :name outfile: Name of the output file to which the generated plots
                  will be written
        """
        print("--> Generating diagnostics plots for step 8 ...")

        # Create new PDF document
        pdf_pages = PdfPages(outfile)

        # PRNU map
        fig = plt.figure ()
        plt.imshow(data._prnu)
        plt.title("PRNU CKD")
        plt.xlabel("Column number")
        plt.ylabel("Row number")
        plt.colorbar()
        pdf_pages.savefig(fig)
        plt.close()

        # Histogram plot of PRNU
        fig = plt.figure ()
        plt.hist(data._prnu.flatten(), bins=100, facecolor='g', normed=1)
        plt.title("Distribution of PRNU CKD values")
        pdf_pages.savefig(fig)
        plt.close()

        # Write the PDF document to the disk
        pdf_pages.close()
