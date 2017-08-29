from distutils.core import setup
from Cython.Build import cythonize
import numpy

print (numpy.get_include())
setup(
    ext_modules=cythonize("noveldist.pyx",include_path=[numpy.get_include()]),
)


def novel_distance(a,b):
    from numpy import ones, sqrt, sum
    dist = ones(89) * 500
    for id in range(len(a)):
        if int(a[id]) == -99 and int(b[id]) == -99:
            dist[id] = 0
        elif int(a[id]) != -99 and int(b[id]) != -99:
            dist[id] = a[id] - b[id]
    return sqrt(sum(dist**2))
	
#def time_test():
#	for id in range(50000):
#		novel_distance(np.random.rand(89,1),np.random.rand(89,1))