#! /usr/bin/env python

import numpy as np
import matplotlib as mpl

def show_array (x):
    """ Display the basic properties of the array.
    """
    print '-- Array dimensions =', x.ndim
    print '-- Array shape      =', x.shape
    print '-- Array datatype   =', x.dtype
    print '-- Array data       =\n', x

## Generate arrays used for testing

arr2d = np.random.rand(4,4)
arr3d = np.random.rand(4,4,4)

## Summary of array properties

show_array(arr2d)
show_array(arr3d)

## Test slicing of arrays

print '\nTest slicing of arrays:'

print '\n-- arr2d[:2,:2]\n', arr2d[:2,:2]
print '\n-- arr2d[1:3,1:3]\n', arr2d[1:3,1:3]

print '\n-- arr3d[:2,:2]',    arr3d[:2,:2].shape,    '\n', arr3d[:2,:2]
print '\n-- arr3d[:2,:2,:2]', arr3d[:2,:2,:2].shape, '\n', arr3d[:2,:2,:2]
print '\n-- arr3d[1,:2,:2]',  arr3d[1,:2,:2].shape,  '\n', arr3d[1,:2,:2]

## Test working with masked arrays

print '\nTest masking of arrays:'

arrMask = np.zeros(arr2d.shape, int)
ma = np.ma.masked_array(arr2d, arrMask)

#print '-- Data array =', arr2d
print '-- Masked array ', ma
print '-- Masked array mean ', ma.mean()

for n in range(ma.shape[1]):
    print 'Column', n, '=', ma[:,n], '-> mean =', ma[:,n].mean()
