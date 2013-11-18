
##______________________________________________________________________________
## Import Python modules

import numpy as np

##______________________________________________________________________________
## Set up description of detector coordinates

detector_dimensions = (5,10)
coords_row = np.array(range(detector_dimensions[0]))
coords_col = np.array(range(detector_dimensions[1]))
yval,xval = np.meshgrid (coords_row, coords_col)

##______________________________________________________________________________
## Calculations based on the grid

z = np.sin(xval**2 + yval**2)/(xval**2 + yval**2)

##______________________________________________________________________________
## Debugging feedback

print '-- Detector dimensions =', detector_dimensions
print '-- Coordinates column  =', coords_row
print '-- Coordinates rows    =', coords_col

print '-- Circular sin function', z

h = plt.contour(coords_col, coord_row, z)
