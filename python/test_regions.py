#! /usr/bin/env python

## =============================================================================
##
##  Global variables
##
## =============================================================================

# Dimensions of the CCD area per band
band1 = [ slice(0,1025,1), slice(0,800,1) ]
band2 = [ slice(0,1025,1), slice(0,800,1) ]
frame = [ band1, band2 ]

# Region selected for processing

selection       = [ slice(500,1000,1), slice(600,1000,1) ]
selection_shape = [ selection[0].stop-selection[0].start, selection[1].stop-selection[1].start ]
region_slices   = [selection,selection]

## =============================================================================
##
##  Debugging feedback
##
## =============================================================================

print "\nInput data:"
print "-- Dimensions band 1 =", band1
print "-- Dimensions band 2 =", band2
print "-- Dimensions frame  =", frame
print "-- Pixel selection   =", selection
print "-- Selection shape   =", selection_shape

## =============================================================================
##
##  Process selection
##
## =============================================================================

if ( selection[1].stop <= frame[0][1].stop ):
    print "--> Selection contains pixels from band 1 only"
    region_slices[1] = False
else:
    if (selection[1].start > frame[0][1].stop):
        print "--> Selection from band 2 only."
        region_slices[0]    = False
        region_slices[1][1] = slice(selection[1].start-frame[0][1].stop,
                                    selection[1].stop-frame[0][1].stop, 1)
    else:
        print "--> Selection spanning both bands."
        tmp = []
        tmp.append([ selection[0], slice(selection[1].start, frame[0][1].stop, 1) ])
        tmp.append([ selection[0], slice(0,selection[1].stop-frame[0][1].stop, 1)])
        region_slices = tmp

print "\nResulting region slices:"
print "-- Region slices[0] =", region_slices[0]
print "-- Region slices[1] =", region_slices[1]
