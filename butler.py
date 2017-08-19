#!python3

import os
import sys
import pathlib as pl
import subprocess as sub


print("Butler V0.00")

have_conanfile   = pl.Path('conanfile.txt').is_file()
have_conanrecipe = pl.Path('conanfile.py' ).is_file()

def extract_requirements(info):
    """Extracts the list of dependencies from the output of "conan info ." (supplied as a string)."""
    reqs = []
    # TODO: the following traversal algorithm could be generalized
    branch = []
    last_indent = -1
    for line in [_.rstrip() for _ in info.split("\n")]:
        print(">", line)
        data = line.lstrip()
        indent = len(line) - len(data)
        if indent > last_indent:
            branch.append((data, indent))
            last_indent = indent
        elif indent == last_indent:
            branch[-1] = (data, indent)
        elif indent < last_indent:
            while True:
                branch.pop()
                if indent >= branch[-1][1]: 
                    last_indent = indent
                    break
        parent = [_[0] for _ in branch[:-1]]
        if parent == ["PROJECT", "Requires:"]:
            yield data
    
def display_conan_info():
    cp = sub.run("conan info .", stdout=sub.PIPE, stderr=sub.PIPE)
    if cp.returncode == 0:
        print("Dependencies:")
        for _ in extract_requirements(cp.stdout.decode()):
            print(_)
    else:
        print("error!")
        print(cp.stdout.decode(), cp.stderr.decode())


if have_conanfile and have_conanrecipe:
    print("CAUTION! This directory has both a conanfile and a conan recipe, aborting for safety")
    sys.exit()
if have_conanfile:
    print("Conanfile found, querying info...")
    display_conan_info()
elif have_conanrecipe:
    print("Conan recipe found, querying info...")
    display_conan_info()
