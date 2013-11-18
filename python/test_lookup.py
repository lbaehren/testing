import numpy as np
import matplotlib.pyplot as plt

## Compute table values
x = np.arange(-10, 10, 0.5)
y = np.sin(x)
nofPoints = x.size
a = np.array ([x,y])

print "-- Size of x  =", x.size
print "-- Size of y  =", y.size
print "-- Size of a  =", a.size
print "-- Shape of a =", a.shape

for to_find in ():
    pos = bisect.bisect_right(x, (to_find,))
    print to_find,"->", pos, "=", x[pos]

xvals = np.array([0.3, 0.6, 0.9, 1.2, 1.5])
yinterp = np.interp(xvals, x, y)

for n in range(xvals.size):
    print xvals[n],"->",yinterp[n]

plt.plot(x, y, '-x')
plt.plot(xvals, yinterp, 'o')
plt.show()
