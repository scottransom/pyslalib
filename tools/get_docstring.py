# -*- coding: utf-8 -*-
"""Convert SLALIB Fortran comments into python docstrings.

F2PY doesn't add descriptive docstrings to Fortran functions that it
wraps. This module will read Fortran comments from SLALIB Fortran
files and then save them as docstrings.
"""
# Extract name from the first line; names are sla_*.
# The line just before comment starts with *+ and the line just after
# the last line starts with *-
# Strip off license information?
# Note:
# dh2e.f function name is dh2e but comment head is D E 2 H
import re
import glob
from argparse import ArgumentParser
import pickle
import json

def get_docstring(filenames: str) -> dict[str, str]:
    name_pattern = r"(sla_\w+)" # names are sla_xxxx
    name_regex = re.compile(name_pattern)
    START = "*+"
    END = "*-"
    doc_dict = {}
    
    for filename in filenames:
        try:
            f = open(filename, "r")
            
            name_line = f.readline() # first line has name
            if name_line[0] == '#': # sla_config line in gresid.F
                name_line = f.readline()
            matches = name_regex.search(name_line)

            if not matches:
                continue

            if len(matches.groups()) != 1: # there should be only one match
                raise ValueError("More than one match for function name.")
            name = matches.group()
            
            doc = []
            inside = 0
            for line in f:
                if inside:
                    doc.append(line)
                elif line[0:2] == START:
                    inside = 1
                if line[0:2] == END:
                    inside = 0
                    del doc[-1] # delete line with "*-"
                    break
            
            # add filename to docstring
            str_to_append = "File: "+ filename + '\n"""'
            doc_dict[name.lower()] = "".join(['"""\n']+doc+[str_to_append])
        finally:
            f.close()
        
    return doc_dict

if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument("-i", "--input", nargs="*")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    docstrings = get_docstring(glob.glob("src/*.[fF]"))
    
    with open(args.output, "w+") as f:
        json.dump(docstrings, f)
        # pickle.dump(docstrings, f)
