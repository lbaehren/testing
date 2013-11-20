import numpy as np

## Generalized sin() function

def Sin (x,
         a0=0.0,
         a1=1.0,
         a2=1.0,
         a3=0.0):
    """ Generalized sin function, including offsets and scale factors.
    """
    return a0+a1*np.sin(a2*x+a3)
