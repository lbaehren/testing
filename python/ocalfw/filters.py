import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

""" Collection of filter windows. """

## =============================================================================
##
##  2D Moving average filter
##
## =============================================================================

def moving_average_2d(shape):
    ## Check input parameter
    if (len(shape)<2):
        print ("ERROR - moving_average_2d needs shape consiting of 2 axes!")
        return []

    # Initialize arrays
    w = np.ones(shape=shape)/np.prod(shape)
    return w


## =============================================================================
##
##  2D Hanning filter
##
## =============================================================================

def hanning_window_2d(shape,
                      normalize=True):
    """ Calculate weights for (normalized) 2D Hanning filter window.

        :param shape: Shape of the 2D Hanning window.
        :type shape: Integer array, size=2
        :param normalize: Normalize the weights of the Hanning window? The
                          underlying NumPy/SciPy method returns an array of
                          values, which does not hold the condition that the
                          sum of all entries equals 1.
        :type normalize: Bool
    """
    # Check input parameter
    if (len(shape)<2):
        print ("ERROR - hanning_window_2d needs shape consiting of 2 axes!")
        return []

    # Initialize arrays
    hanning_row = np.hanning(shape[0])
    hanning_col = np.hanning(shape[1])
    hanning2d   = np.ndarray(shape=shape)

    for nrow in range(shape[0]):
        hanning2d[nrow, :] = hanning_col

    for ncol in range(shape[1]):
        hanning2d[:, ncol] = hanning2d[:, ncol]*hanning_row

    if (normalize):
        hanning2d_norm = hanning2d/np.sum(hanning2d)
        return hanning2d_norm
    else:
        return hanning2d

##  Testing

if __name__ == '__main__':

    shape = (256, 256)
    hanning2d      = hanning_window_2d(shape)
    moving_average = moving_average_2d(shape)

    ## Create new PDF document
    pdf_pages = PdfPages('plots_filters.pdf')

    fig = plt.figure ()
    plt.imshow(hanning2d)
    plt.title("2D Hanning window")
    pdf_pages.savefig(fig)
    plt.close()

    fig = plt.figure ()
    plt.imshow(moving_average)
    plt.title("2D moving average filter")
    pdf_pages.savefig(fig)
    plt.close()

    # Write the PDF document to the disk
    pdf_pages.close()

