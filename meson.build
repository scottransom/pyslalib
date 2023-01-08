# Thanks to SciPy project for initial meson.build file!
project(
  'pyslalib',
  'c',
  version: '1.0',
  license: 'GPLv2',
  meson_version: '>= 0.62',
  default_options: [
    'buildtype=debugoptimized',
    'c_std=c99',
    'c_args=-Wno-unused-function -Wno-conversion -Wno-misleading-indentation -Wno-incompatible-pointer-types -Wunused-variable',
    'fortran_args=-Wno-conversion -Wunused-dummy-argument -Wno-unused-function -Wunused-variable',
    'fortran_std=legacy',
  ],
)

# Find C/C+ compilers separately from Fortran compiler
cc = meson.get_compiler('c')

# Adding at project level causes many spurious -lgfortran flags.
add_languages('fortran', native: false)
fc = meson.get_compiler('fortran')

# Compiler-dependent arguments
GCC = cc.get_id() == 'gcc'
GFORTRAN = fc.get_id() == 'gcc'
CC_FLAGS = []
CC_LINK_FLAGS = []
FC_FLAGS = []
FC_LINK_FLAGS = []

# TODO: Make flags for VC and Intel compilers

if GCC
  CC_FLAGS += [
    '-DDEBUG',
    '-fopenmp'
  ]
  CC_LINK_FLAGS += [
    '-lgomp',
    '-lquadmath',
  ]
endif

# Although, gfortran has the same flags as gcc, here we specify them
# separately, because gfortran might be used along with MSVC compiler 
if GFORTRAN
  if not GCC
    CC_FLAGS += [
      '-DDEBUG',
      '-fopenmp'
    ]
  endif
  FC_LINK_FLAGS += [
    '-lgomp',
    '-lquadmath',
  ]
endif

# Platform-dependent flags
WINDOWS = build_machine.system() == 'windows'
MINGW = WINDOWS and GCC

if WINDOWS and not GCC
  error('Currently, libsla could be built only with GCC toolchain on Windows')
endif

if MINGW
  # Probably, -DSIZEOF_VOID_P=8 is not neccessarty with -DMS_WIN64
  MINGW_FLAGS = [
    '-DSIZEOF_VOID_P=8',
    '-DMS_WIN64'
  ]
  MINGW_LINK_FLAGS = [ 
    '-static-libgcc', 
    '-static-libstdc++', 
    '-static', 
    '-static-libgfortran',
  ]
  CC_FLAGS += MINGW_FLAGS
  FC_FLAGS += MINGW_FLAGS
  CC_LINK_FLAGS += MINGW_LINK_FLAGS
  FC_LINK_FLAGS += MINGW_LINK_FLAGS
endif

# This argument is called -Wno-unused-but-set-variable by GCC, however Clang
# doesn't recognize that.
if cc.has_argument('-Wno-unused-but-set-variable')
  CC_FLAGS += ['-Wno-unused-but-set-variable']
endif

# Find python module (src: https://mesonbuild.com/Python-module.html)
py3 = import('python').find_installation()
py3_dep = py3.dependency() # In newer versions, Python 3 dependency by default
py3_venv_dir = run_command(
  py3.full_path(),
  ['-c', 
    'import sys; print(sys.prefix)'
  ], 
  check: true).stdout().strip()
py3_base_dir = run_command(
  py3.full_path(),
  ['-c', 
    'import sys; print(sys.base_prefix)'
  ], 
  check: true).stdout().strip()

meson_src_base_dir = meson.current_source_dir()

# Dependencies for modules/submodules/extensions
deps = [py3_dep]

# Link import library on Windows when using gcc
if MINGW
  dirs = [
    py3_venv_dir / 'Lib',
    py3_venv_dir / 'libs',
    py3_venv_dir / 'Library',
    py3_base_dir / 'Lib',
    py3_base_dir / 'libs',
    py3_base_dir / 'Library',
  ]
  py_str_version = py3.language_version().replace('.', '')
  libpython_name = 'python' + py_str_version
  libpython = cc.find_library(libpython_name, 
                              dirs: dirs, 
                              required : true)
  deps += [libpython,]
endif

# Finalize the compiler and linker arguments
add_global_arguments(CC_FLAGS, language : 'c')
add_project_link_arguments(CC_LINK_FLAGS, language : 'c')
add_global_arguments(FC_FLAGS, language : 'fortran')
add_project_link_arguments(FC_LINK_FLAGS, language : 'fortran')

# Find F2py and related tools

f2py_mod = files('./tools/f2py_mod.py')
incdir_f2py = run_command(
  py3,
  [
    '-c',
    'import os; import numpy.f2py as f; print(os.path.realpath(f.get_include()))'
  ],
  check : true
).stdout().strip()

# F2py needs the Numpy headers to compile the Fortran extensions.
# (src: https://numpy.org/devdocs/f2py/buildtools/meson.html)
incdir_numpy = run_command(
  py3,
  [
    '-c', 
    'import os; import numpy as np; print(os.path.realpath(np.get_include()))'
  ],
  check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
inc_f2py = include_directories(incdir_f2py)

# Do not use deprecated Numpy API
numpy_nodepr_api = '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION'
CC_FLAGS += [numpy_nodepr_api]
FC_FLAGS += [numpy_nodepr_api]

# Make fortranobject from F2py as Fortran extension dependency 
fortranobject_c = incdir_f2py / 'fortranobject.c'

# Share this object across multiple modules.
fortranobject_lib = static_library(
  'fortranobject',
  fortranobject_c,
  dependencies: deps,
  include_directories: [inc_np, inc_f2py]
)
fortranobject_dep = declare_dependency(
  link_with: fortranobject_lib,
  include_directories: [inc_np, inc_f2py]
)
deps += fortranobject_dep

# Append meson.build file in apex root source folder
subdir('src')
subdir('pyslalib')
