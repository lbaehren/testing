import h5py
import numpy as np

## Open/create HDF5 file

f = h5py.File("test_h5py.h5", "w")

## Create dataset and display its properties

dataset1 = f.create_dataset("mydataset", (100,), dtype='i')

print '- Dataset name  =',  dataset1.name
print '- Dataset shape =',  dataset1.shape
print "- Dataset dtype = ", dataset1.dtype

## Create dataset from NumPy Array

x = np.array([[1,2,3],[4,5,6],[7,8,9]], int)

dataset2 = f.create_dataset("array_2d", x.shape, dtype='i')
dataset2[:] = x

print "- Properties dataset 2:"
print '  - Name  =',  dataset2.name
print '  - Shape =',  dataset2.shape
print "  - Dtype = ", dataset2.dtype
