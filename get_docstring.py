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

def get_docstring():
    name_pattern = r"(sla_\w+)" # names are sla_xxxx
    name_regex = re.compile(name_pattern)
    START = "*+"
    END = "*-"
    doc_dict = {}
     
    file_list = glob.glob('*.[fF]')
     
    print("%d files found." % len(file_list))
     
    for i,file_name in enumerate(file_list):
        f = open(file_name, "r")
        
        name_line = f.readline() # first line has name
        if name_line[0] == '#': # sla_config line in gresid.F
            name_line = f.readline()
        matches = name_regex.search(name_line)
        if len(matches.groups()) != 1: # there should be only one match
            raise ValueError("More than one match for function name.")
        name = matches.group()
        print("Reading %10s in %s." % (name, file_name))
        
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
        str_to_append = "File: "+ file_name + '\n"""'
        doc_dict[name.lower()] = "".join(['"""\n']+doc+[str_to_append])
     
        f.close()
        
    print("%d functions read from %d files." % (len(doc_dict), len(file_list)))
    return doc_dict

if __name__ == "__main__":
    docstrings = get_docstring()
