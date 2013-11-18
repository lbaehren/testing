#! /usr/bin/env python

## Dictionary with the bands per detector CCD
bands = {'1': (1, 2), '3': (5, 6), '2': (3, 4), '4': (7, 8)}
## Region selections per CCD
selected_regions = {1: [(10,90),(200,310)],   ## [(x_start,x_stop),(y_start,y_stop)]
                    2: [(20,90),(200,310)],
                    3: [(30,90),(200,310)],
                    4: [(40,90),(200,310)]}

## =============================================================================
##
##  Dictionary testing
##
## =============================================================================

print "\nDictionary testing\n"

process_bands = [1,3,4];

## Control feedback
print '-- Process bands        =', process_bands
print '-- nof. detector CCDs   =', len(bands)

for k,v in bands.items():
    print '-- Band for detector', k, ' =', v


## Inspect list of bands to process
for k,v in bands.items():
    if (v[0] in process_bands) and (v[1] in process_bands):
        print "--> Processing bands", v, 'for detector', k

## =============================================================================
##
##  Region testing
##
## =============================================================================

print "\nRegion testing\n"

def region2slice (regionCorners,
                  groupedByAxis=True,
                  debugging=False):
    """ Convert region parameters to slice.
    """
    nofAxes=len(regionCorners)
    slices=[]
    ## Debugging output
    if debugging:
        print '[region2slice] Input data:'
        print '-- Region corners   =',regionCorners
        print '-- Grouped by axis  =',groupedByAxis
        print '-- nof. region axes =',nofAxes
    ## Convert region definition to slices
    if groupedByAxis:
        for n in range(nofAxes):
            slices.append(slice(regionCorners[n][0],regionCorners[n][1]))
    else:
        print 'Sorry - alternate input ordering not yet implemented!'
    ## Return result of the conversion
    return slices

## Print available region parameters
for k,v in selected_regions.items():
    print '-- Region for detector', k, '=', v


print '-- Selection slice =',[slice(10,100), slice(20,200)]

print region2slice(selected_regions[1])
print region2slice(selected_regions[2])
