#!python

import os
import sys
import pathlib as pl
import subprocess as sub
from lib.indented_text_parser import IndentedTextParser
from lib.grips import *
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


# The main routine

def main():
    print("Gaffer V0.0") # TODO: extract version from single source

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    p_info   = subparsers.add_parser('info', help="Display general info about the current working directory")
    p_remsub = subparsers.add_parser('remove-submodule')
    p_remsub.add_argument('submodule')

    ns = parser.parse_args()
    #print("subcommand: %s" % ns.subcommand)
    
    try:
        if ns.subcommand == 'remove-submodule':
            remove_submodule(ns)
        elif ns.subcommand == 'info':
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
            GitGrip.display_info()
    except Exception as e:
        print("Command failed: %s" % e)

if __name__ == "__main__":
    main()