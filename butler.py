#!python

import os
import sys
import pathlib as pl
import subprocess as sub
from lib.indented_text_parser import IndentedTextParser
from git import Repo


def extract_requirements(info):
    parser = IndentedTextParser()
    for _ in parser.parse_string(info):
        #print(":", _)
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
            print("  %s" % _)
    else:
        print("error!")
        print(cp.stdout.decode(), cp.stderr.decode())


def display_git_info():
    if not pl.Path('.git').is_dir():
        print("This directory is not a (non-bare) git repository")
    else:
        print("Directory is a git repository, obtaining info...")
        repo = Repo('.')
        if repo.is_dirty(): print("Repository is dirty!")
        if not repo.untracked_files:
            print("No untracked files")
        else:
            print("Untracked files:")
            for _ in repo.untracked_files: 
                print("  %s" % _)
        if not repo.submodules:
            print("No submodules")
        else:
            print("Submodules:")
            for _ in repo.submodules: 
                print("  %s" % _)
    
    
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
    display_git_info()

if __name__ == "__main__":
    main()