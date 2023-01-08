"""Python interface to SLALIB.

This module, pyslalib, is a f2py-generated (and hand-tweaked to
eliminate unnecessary function/subroutine arguments) wrappers for the
Fortran version of P.T. Wallace's SLALIB positional astronomy library.

The python wrappers cover every function in SLALIB and a comprehensive
set of unit tests are available in the test/ directory of the source
distribution.  The only external dependency is numpy.

The module ``pyslalib.slalib`` contains the f2py wrapped
functions. Call of ``help("sla_dat")`` will return a string
containing the documentation for the ``sla_dat`` function. The
documentation for each function is generated from the comment at the
beginning of the SLALIB Fortran source file.
"""
import os
from . import slalib as sla
import json


PACKAGE_DIR = os.path.dirname(__file__)
with open(os.path.join(PACKAGE_DIR, "docstrings.json"), "r") as f:
    docstrings_map = json.load(f)


__all__ = []


# Add docstrings and strip sla_ prefix from function names
for obj_name, obj in sla.__dict__.items():
    if hasattr(obj, "__call__"):
        obj.__doc__ = docstrings_map.get(obj_name, getattr(obj, "__doc__", ""))
        globals()[obj_name] = obj
        __all__.append(obj_name)

