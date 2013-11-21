import numpy as np

## =============================================================================
##
##  2D Moving average filter
##
## =============================================================================

## =============================================================================
##
##  2D Hanning filter
##
## =============================================================================

def HanningWindow2D(shape,
                    normalize=True):
    """ Calculate weights for (normalized) 2D Hanning filter window.
    """
    ## Check input parameter
    if (len(shape)<2):
        print ("ERROR - HanningWindow2D needs shape consiting of 2 axes!")
        return []

    ## Initialize arrays
    hanning_row = np.hanning(shape[0])
    hanning_col = np.hanning(shape[1])
    hanning2d   = np.ndarray(shape=shape)

    for nrow in range(shape[0]):
        hanning2d[nrow,:] = hanning_col

    for ncol in range(shape[1]):
        hanning2d[:,ncol] = hanning2d[:,ncol]*hanning_row

    if (normalize):
        hanning2d_norm = hanning2d/np.sum(hanning2d)
        return hanning2d_norm
    else:
        return hanning2d
