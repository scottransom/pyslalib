#  Makefile for SLALIB
#   for Pentium/Linux
#   by Scott M. Ransom

# OS type
OS = Linux
#OS = OSX

# Linux is the first choice
ifeq ($(OS),Linux)
	LIBSUFFIX = .so
	LIBCMD = -shared
	SYSDIR = /usr
	LOCDIR = /usr/local
# else assume Darwin (i.e. OSX)
else
	LIBSUFFIX = .dylib
	LIBCMD = -dynamiclib
	SYSDIR = /sw
	LOCDIR = /sw
endif

CC = gcc
FC = gfortran
#FC = g77
CFLAGS = -O2 -Wall -W -fPIC
CLINKFLAGS = $(CFLAGS)
FFLAGS = -O2 -fPIC
FLINKFLAGS = $(FFLAGS)

all: slalib

slalib: libsla$(LIBSUFFIX)
	$(FC) -o test/sla_test test/sla_test.f -fno-second-underscore -L. -lsla
	test/sla_test

libsla$(LIBSUFFIX):
	$(FC) $(FFLAGS) -fno-second-underscore -c -I. *.f *.F
	$(FC) $(LIBCMD) -o libsla$(LIBSUFFIX) -fno-second-underscore *.o

# Note:  a better way to make pyslalib is to use the setup.py file
pyslalib:
	f2py -c slalib.pyf -I. *.f *.F

clean:
	rm -f *.o *~ *# 
	rm -rf build

cleaner: clean
	rm -f test/sla_test libsla.so slalib.so
