import numpy as np
from scipy.interpolate import griddata
import matplotlib as mpl

## =============================================================================
##
##  Test functions
##
## =============================================================================

# Create array with the original position coordinates (nrow,ncol)
detector_dimensions = (10,35)
data = np.random.rand(detector_dimensions[0],detector_dimensions[1])
mask = np.ones(data.shape)

masked_data = np.ma.masked_array (data, mask=mask)
selected_data = data[data>0.5]

row_positions = np.array(range(detector_dimensions[0]))
col_positions = np.array(range(detector_dimensions[1]))

# Debugging feedback
print 'Detector dimensions =', detector_dimensions
print 'Detector data shape =', data.shape, "->", data.size
print 'Masked data ....... =', masked_data.shape, "->", masked_data.size
print 'Selected data ..... =', selected_data.shape

##
## Code example: 2D Interpolation of Large Irregular Grid to Regular Grid
##

def example1():
    print ("\n[Example 1]\n")
    ## Create indices for x and y axis
    y,x = np.indices([2048,2048],dtype='float64')
    z   = np.random.randn(2048,2048)
    yr  = y + np.random.randn(2048,2048)
    xr  = x + np.random.randn(2048,2048)
    zn  = griddata(xr.ravel(),yr.ravel(),z.ravel(),x,y)
    #zl  = griddata(xr.ravel(),yr.ravel(),z.ravel(),x,y,interp='linear')

## =============================================================================
##
##  Main routine
##
## =============================================================================

example1()
