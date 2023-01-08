# pySLALIB v1.1.0  (Jan 2023)

pySLALIB provides interface for the Fortran version of P.T. Wallace's SLALIB positional astronomy 
library via f2py-generated (and hand-tweaked to eliminate unnecessary function/subroutine 
arguments) wrappers. SLALIB used to be hosted by the STARLINK site, although that service has been 
suspended. The version of SLALIB included here is 2.5-4 (with several additional tweaks) and is 
released under the GPL.

The python wrappers cover every function in SLALIB and a comprehensive
set of unit tests are available in the test/ directory.  The only
external dependency is numpy (http://numpy.scipy.org).  These wrappers
are not related to the older (and apparently abandoned) pySLALIB that
was once available on the Web (and which depended on Numeric as
opposed to numpy).

Note: this version supports Windows (user must install mingw64-toolkit before building pySLALIB).


# Build

**Note: if not stated, commands are executed from repository directory.**

- ## Windows
    Since version 1.1.0 building the pySLALIB is supported under Windows. This is available due 
    to new build system `meson-python` via MinGW64 toolchain set of GCC compilers and libraries.
    
    ### Prerequisites
    - msys2 (https://www.msys2.org/)
    - mingw64-w64-toolchain (`pacman -Syu mingw64-w64-toolchain` from MSYS2 terminal)

    ###  Steps
    1. Add E:\Programs\msys64\usr\bin (example path to /usr/bin directory in MSYS2 installation) 
    to the PATH (powershell example):
        ```
        $Env:PATH="E:\Programs\msys64\usr\bin;" + $PATH
        ```
    2. Install python dependencies:
        ```
        pip install -r requirements.txt
        ```
    2. Run build:
        ```
        python -m build -w -n .
        ```

- ## Linux (Ubuntu 2x.04)
    pySLALIB natevily supports Linux.

    ### Prerequisites
    - python3-pip
    - build-essential
    - gfortran

    ### Steps
    1. Install system dependencies:
        ```
        sudo apt install build-essential python3-pip gfortran
        ```
    2. Install python dependencies:
        ```
        pip install -r requirements.txt
        ```
    3. Run build:
        ```
        python -m build -w -n .
        ```

All built wheels (`.whl` files) will be placed to the directory dist under current repository if 
parameter `-o` is not provided in #3 step. Note, tags are already passed all tests before uploading.


# Installation

Most users will only need to do:
```
pip install <name-of-the-pyslalib-wheel>.whl
```

to generate the wrappers, build, and install the package. **This method is preferrable since 
binary distributions are already uploaded for platforms Windows X86-64 and Linux X86-64.** 
Otherwise one should build the packages before proceeding to the installation (see previous section).

Once pySLALIB is installed, you can run the unittests via:
```
  > python test/test_slalib.py
```

# Example Usage (using IPython)

```
In [1]: import pyslalib as slalib

In [2]: slalib.sla_veri()
Out[2]: 2005004

In [3]: slalib.sla_caldj(1999, 12, 31)
Out[3]: (51543.0, 0)

In [4]: slalib.sla_etrms(1976.9)
Out[4]: array([ -1.62161710e-06,  -3.31007009e-07,  -1.43529663e-07])

In [5]: slalib.sla_fk45z(1.234, -0.123, 1984)
Out[5]: (1.2446165107316911, -0.12141858395865548)

In [6]: slalib.sla_dafin("-00 03 34.6", 1)
Out[6]: (12, -0.0010404101596610642, 0)

In [7]: slalib.sla_obs(0, "GBT")
Out[7]:
('GBT',
 'Green Bank Telescope                    ',
 1.3934679949996727,
 0.67078450520692623,
 880.0)
```

You can print the original Fortran doc strings using something like:

```
In [1]: from pyslalib import sla_caldj

In [2]: sla_caldj?
"""
*     - - - - - -
*      C A L D J
*     - - - - - -
*
*  Gregorian Calendar to Modified Julian Date
*
*  (Includes century default feature:  use sla_CLDJ for years
*   before 100AD.)
*
*  Given:
*     IY,IM,ID     int    year, month, day in Gregorian calendar
*
...
```



If you find any problems, please sent message to original developer Scott M. Ransom 
<sransom@nrao.edu> or this version contributor Nicolai S. Pankov <nspankov@edu.hse.ru>
