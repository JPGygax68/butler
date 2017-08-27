#!python

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
    
    for sc in subcommands: sc.define_subparser(subparsers)
    
    ns = parser.parse_args()
    #print("subcommand: %s" % ns.subcommand)
    
    try:
        for sc in subcommands:
            if ns.subcommand == sc.name:
                sc.execute(ns)
    except Exception as e:
        print("Command failed: %s" % e)


if __name__ == "__main__":
    main()