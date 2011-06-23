"""Python interface to SLALIB.

This module, pyslalib, is a f2py-generated (and hand-tweaked to
eliminate unnecessary function/subroutine arguments) wrappers for the
Fortran version of P.T. Wallace's SLALIB positional astronomy library.

The python wrappers cover every function in SLALIB and a comprehensive
set of unit tests are available in the test/ directory of the source
distribution.  The only external dependency is numpy.

The module ``pyslalib.slalib`` contains the f2py wrapped
functions. The dictionary, ``pyslalib.sladoc`` contains documentation
for functions; accessed by using the function name as key. For
example: ``pyslalib.sladoc['sla_dat']`` will return a string
containing the documentation for the ``sla_dat`` function. The
documentation for each function is generated from the comment at the
beginning of the SLALIB Fortran source file.
"""
import pickle
import os

# Relative path: from .slalib import *
# works for 2.6 and above but we use this form to work on 2.5
from pyslalib import slalib

# A dictionary with functions as keys and comments in SLALIB
# Fortran files as value strings. Use 
dir_name = os.path.dirname(slalib.__file__)
f = open(os.path.join(dir_name,"docstring_pickle.pkl"), "rb")
sladoc = pickle.load(f)
