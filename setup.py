#!/usr/bin/env python
import glob
from numpy.distutils.core import setup, Extension

ext1 = Extension(name = 'slalib',
                 include_dirs = ['.'],
                 sources = ['slalib.pyf']+\
                           glob.glob("*.f")+\
                           glob.glob("*.F"))

if __name__ == "__main__":
    setup(name = 'pySLALIB',
          description       = "f2py and numpy based wrappers for SLALIB",
          version           = "1.0.1",
          author            = "Scott Ransom",
          author_email      = "sransom@nrao.edu",
          ext_modules = [ext1]
          )
