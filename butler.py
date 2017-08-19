#!python

import os
import sys
import pathlib as pl
import subprocess as sub
from lib.indented_text_parser import IndentedTextParser


def extract_requirements(info):
    parser = IndentedTextParser()
    for _ in parser.parse_string(info):
        print(":", _)
        if _[0] == 0 and _[1][:-1] == ['PROJECT', 'Requires:']:
            yield _[1][-1]

print("Butler V0.0")

have_conanfile   = pl.Path('conanfile.txt').is_file()
have_conanrecipe = pl.Path('conanfile.py' ).is_file()

def display_conan_info():
    cp = sub.run("conan info .", stdout=sub.PIPE, stderr=sub.PIPE)
    if cp.returncode == 0:
        print("Dependencies:")
        for _ in extract_requirements(cp.stdout.decode()):
            print(_)
    else:
        print("error!")
        print(cp.stdout.decode(), cp.stderr.decode())


# The main routine

def main():
    if have_conanfile and have_conanrecipe:
        print("CAUTION! This directory has both a conanfile and a conan recipe, aborting for safety")
        sys.exit()
    if have_conanfile:
        print("Conanfile found, querying info...")
        display_conan_info()
    elif have_conanrecipe:
        print("Conan recipe found, querying info...")
        display_conan_info()

if __name__ == "__main__":
    main()