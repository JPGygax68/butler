#!python

import os
import sys
import pathlib as pl
import subprocess as sub
from lib.indented_text_parser import IndentedTextParser
from git import Repo
import argparse


# TODO: normalize modules to return information as nested dictionaries ?


def extract_requirements(info):
    parser = IndentedTextParser()
    for _ in parser.parse_string(info):
        #print(":", _)
        if _[0] == 0 and _[1][:-1] == ['PROJECT', 'Requires:']:
            yield _[1][-1]

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
        print("Active branch: %s" % repo.active_branch)
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
                if _.module_exists(): 
                    print("    Module is available")
                    sm = _.module()
                    print("    Working tree directory: %s" % sm.working_tree_dir)
                    print("    Branches: %s" % ', '.join([
                        ('*' if _ == sm.active_branch else '') + str(_) for _ in sm.branches]))
                    #print("      Active branch: %s" % sm.active_branch)
                    #for br in sm.branches:
                    #    print("      %s" % br)
                else:
                    print("    Module is NOT available")
        if not any(_ for _ in repo.index.entries.items() if _[0][1] != 0):
            print("No uncommitted changes")
        else:
            print("Index:")
            for (path, stage), entry in repo.index.entries.items():
                if stage != 0:
                    print("  %s: %s" % (path, stage))
    
    
# The main routine

def main():
    print("Butler V0.0")

    ap = argparse.ArgumentParser()
    ap.add_argument("info", help="Display general info about the current directory")
    ap.parse_args()

    have_conanfile   = pl.Path('conanfile.txt').is_file()
    have_conanrecipe = pl.Path('conanfile.py' ).is_file()

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