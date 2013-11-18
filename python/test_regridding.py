import numpy as np
import matplotlib as mpl

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

