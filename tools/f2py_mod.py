import os
import subprocess
import argparse
import shutil
import sys


def _run_f2py(infile: str, outdir: str) -> int:
    _, ext = os.path.splitext(infile)
    if ext != ".pyf":
        raise ValueError("Input wrapper should have .pyf extension.")

    cmd = [
        sys.executable,
        "-m",
        "numpy.f2py",
        infile,
        "--build-dir",
        outdir,
        "--lower",
    ]

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd(),
    )
    _ = p.communicate()
    
    if p.returncode != 0:
        raise RuntimeError(f"Error: f2py returned status {p.returncode}")

    return p.returncode


def main():
    parser = argparse.ArgumentParser(
        "f2py_mod",
        description="Generate C-code from .pyf Fortran wrapper",
    )
    parser.add_argument("-i", "--infile", help="Path to the .pyf wrapper")
    parser.add_argument(
        "-o",
        "--outdir",
        help="Path to the generated C-code and Fortran wrapper",
    )
    args = parser.parse_args()
    outdir_abs = os.path.join(os.getcwd(), args.outdir)

    return _run_f2py(args.infile, outdir_abs)


if __name__ == "__main__":
    sys.exit(main())
