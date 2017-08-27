#!python

import os
import sys
import pathlib as pl
from lib.grips import *
from lib.subcommands import *
import argparse


# TODO: normalize modules to return information as nested dictionaries ?


# The main routine

def main():
    print("Gaffer V0.0") # TODO: extract version from single source

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity')
    subparsers = parser.add_subparsers(dest='subcommand')
    
    # TODO: do this automatically for all subcommands in the subcommands dir
    InfoCommand           .define_subparser(subparsers)
    RemoveSubmoduleCommand.define_subparser(subparsers)
    
    ns = parser.parse_args()
    #print("subcommand: %s" % ns.subcommand)
    
    try:
        if ns.subcommand == 'remove-submodule':
            RemoveSubmoduleCommand.execute(ns)
        elif ns.subcommand == 'info':
            InfoCommand.execute()
    except Exception as e:
        print("Command failed: %s" % e)

if __name__ == "__main__":
    main()