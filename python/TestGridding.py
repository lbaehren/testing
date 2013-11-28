
""" Collection of code examples for working with mesh data, which in the general
    case can be defined on an irregular grid.
"""

import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import scipy.interpolate as sip

## Global constants

image_shape = (10,35)

## =============================================================================
##
##  Helper functions
##
## =============================================================================

##______________________________________________________________________________
##                                                                        Circle

def Circle (x,
            y,
            x0=0.0,
            y0=0.0,
            a0=1.0,
            a1=1.0,
            a2=1.0):
    """ General definition of circle, or rather an ellipse.
        :param x:  x-axis coordinate value.
        :param y:  y-axis coordinate value.
        :param x0: x-axis coordinate of the circle's center position.
        :param y0: y-axis coordinate of the circle's center position.
    """
    r = a0 * np.sqrt(a1*(x-x0)**2 + a2*(y-y0)**2)
    return r

##______________________________________________________________________________
##                                                                        Circle

def Gaussian2D(x,
               y,
               x0=0.0,
               x1=1.0,
               y0=0.0,
               y1=1.0,
               a0=2.0,
               a1=1.0):
    """ 2D Gaussian function.

        :param x: x-axis positions of the points where the function is computed.
        :param y: y-axis positions of the points where the function is computed.
        :param x0: Offset along the x-axis.
        :param y0: Offset along the y-axis.
    """
    return a0*np.exp(-(x-x0)**2/(2*x1)**2-(y-y0)**2/(2*y1)**2)+a1

##______________________________________________________________________________
##                                                            transformation_map

def transformation_map(shape):
    """ Generate map for transformation from detector (row,col) to (row,wavelength)
        grid.
    """
    m = np.ndarray(shape=shape)
    for nrow in range(shape[0]):
        rowValue = 0.5*shape[0]-nrow
        for ncol in range(shape[1]):
            m[nrow,ncol] = Circle(rowValue, 1.5*ncol, y0=0.5*ncol, a0=10)
    return m

## =============================================================================
##
##  Test functions
##
## =============================================================================

##______________________________________________________________________________
##                                                                plot_functions

def plot_functions (pdf_pages,
                    nofPoints=100):
    """ Create plots for the various (mathematical functions.

        :param pdf_pages: PDF document for collecting the generated plots.
        :param nofPoints: Number of points per side of the grid.
    """
    positions = np.mgrid[0:nofPoints, 0:nofPoints]

    valGaussian2D = Gaussian2D(positions[0],
                               positions[1],
                               x0=nofPoints/2.0,
                               y0=nofPoints/2.0,
                               x1=10.0,
                               y1=10.0)
    fig = plt.figure ()
    plt.imshow(valGaussian2D)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("gaussian(x,y)")
    pdf_pages.savefig(fig)
    plt.close()


##______________________________________________________________________________
##                                                                      example1

def example1 ():
    print ("\n[Example 1]\n")
    # Create array with the original position coordinates (nrow,ncol)
    data = np.random.rand(image_shape[0],image_shape[1])
    mask = np.ones(data.shape)

    masked_data = np.ma.masked_array (data, mask=mask)
    selected_data = data[data>0.5]

    row_positions = np.array(range(image_shape[0]))
    col_positions = np.array(range(image_shape[1]))

    # Debugging feedback
    print '-- Detector dimensions =', image_shape
    print '-- Detector data shape =', data.shape, "->", data.size
    print '-- Masked data ....... =', masked_data.shape, "->", masked_data.size
    print '-- Selected data ..... =', selected_data.shape

##______________________________________________________________________________
##                                                                      example2
##
## 2D Interpolation of Large Irregular Grid to Regular Grid

def example2 (pdf_pages):
    print ("\n[Example 2]\n")
    nofPoints=100
    # Create indices for x and y axis
    y,x = np.indices([nofPoints,nofPoints], dtype='float32')
    # Create function values associated with the mesh points
    z   = np.random.randn(nofPoints,nofPoints)
    yr  = y + np.random.randn(nofPoints,nofPoints)
    xr  = x + np.random.randn(nofPoints,nofPoints)
    # Re-gridding of data onto regular grid
    #zn  = griddata(xr.ravel(), yr.ravel(), z.ravel(), x, y)
    #zl  = griddata(xr.ravel(),yr.ravel(),z.ravel(),x,y,interp='linear')

    # Plot the grid points
    print ("--> Creating scatter plot of mesh points ...")
    fig = plt.figure ()
    plt.scatter(xr, yr, marker='x', c='g', s=2)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Scatter plot of (xr,yr) values")
    pdf_pages.savefig(fig)
    plt.close()

##______________________________________________________________________________
##                                                     regrid_transformation_map
##
## Generate grid based on transformation map

def regrid_transformation_map (pdf_pages):
    """ Generate grid based on transformation map. """
    print ("\n[regrid_transformation_map]\n")
    # Get the transformation map
    print ("--> Retrieving transformation map ...")
    m = transformation_map(image_shape)
    # Array holding coordinates of mesh points
    points = np.random.rand(m.size, 2)
    # Compute new set up mash points
    print ("--> Computing mesh points after transform ...")
    count = 0
    for ny in range(m.shape[0]):
        for nx in range(m.shape[1]):
            points[count,0] = ny
            points[count,1] = m[ny,nx]
            count          += 1

    # Create plot of the transformation map
    print ("--> Creating plot for transformation map ...")
    fig = plt.figure ()
    plt.imshow(m)
    plt.xlabel("Column (x)")
    plt.ylabel("Row (y)")
    plt.title("Transformation map (row,col) -> (row,wavelength)")
    pdf_pages.savefig(fig)
    plt.close()

    # Plot the grid points
    print ("--> Creating plot for new set of mesh points ...")
    fig = plt.figure ()
    plt.scatter(points[:,1], points[:,0], marker='x', c='g', s=2)
    plt.xlabel("Wavelength (x)")
    plt.ylabel("Row (y)")
    plt.title("Scatter plot of (row,wavelength) mesh grid")
    pdf_pages.savefig(fig)
    plt.close()

## =============================================================================
##
##  Main routine
##
## =============================================================================

if __name__ == '__main__':

    ## Create new PDF document for collecting the generated plots
    pdf_pages = PdfPages('TestGridding_plots.pdf')

    # Run example routines
    example1()
    example2(pdf_pages)
    regrid_transformation_map(pdf_pages)

    plot_functions(pdf_pages)

    # Write the PDF document to the disk
    pdf_pages.close()
