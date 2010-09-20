pySLALIB v1.0.1  (Sep 2010)
---------------

This is archive contains new f2py-generated (and hand-tweaked to
eliminate unnecessary function/subroutine arguments) wrappers for the
Fortran version of P.T. Wallace's SLALIB positional astronomy library.
SLALIB used to be hosted by the STARLINK site, although that service
has been suspended.  The version of SLALIB included here is 2.5-4
(with several additional tweaks) and is released under the GPL.

The python wrappers cover every function in SLALIB and a comprehensive
set of unit tests are available in the test/ directory.  The only
external dependency is numpy (http://numpy.scipy.org).  These wrappers
are not related to the older (and apparently abandoned) pySLALIB that
was once available on the Web (and which depended on Numeric as
opposed to numpy).

Installation
------------
Most users will only need to do:
  > python setup.py install
to generate the wrappers, build, and install the library.

Once slalib.so has been installed in your PYTHONPATH, you can run the
unittests via:
  > python test/test_slalib.py

Example Usage (using IPython)
-------------
In [1]: import slalib as S

In [2]: S.sla_veri()
Out[2]: 2005004

In [3]: S.sla_caldj(1999, 12, 31)
Out[3]: (51543.0, 0)

In [4]: S.sla_etrms(1976.9)
Out[4]: array([ -1.62161710e-06,  -3.31007009e-07,  -1.43529663e-07])

In [5]: S.sla_fk45z(1.234, -0.123, 1984)
Out[5]: (1.2446165107316911, -0.12141858395865548)

In [6]: S.sla_dafin("-00 03 34.6", 1)
Out[6]: (12, -0.0010404101596610642, 0)

In [7]: S.sla_obs(0, "GBT")
Out[7]:
('GBT',
 'Green Bank Telescope                    ',
 1.3934679949996727,
 0.67078450520692623,
 880.0)

If you would like to build a shared library for linking with other
programs, a simple Makefile is also included that should work with
only minor tweaks for most Unix-like OSs.

Please let me know if you find any problems.

Scott

----------------------------------
Scott M. Ransom <sransom@nrao.edu>
http://www.cv.nrao.edu/~sransom