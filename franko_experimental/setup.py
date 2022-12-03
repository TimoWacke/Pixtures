from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

package = Extension('cy_import', ['franko_experimental/cy_import.pyx'], include_dirs=[numpy.get_include()])
setup(ext_modules=cythonize([package]))