import pathlib as pl
import subprocess as sub
from ..grips import GitGrip
from ..indented_text_parser import IndentedTextParser


# TODO: create a Conan grip and use that instead of calling conan directly


# Private methods

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

        
class InfoCommand:

    name = 'info'
    
    def define_subparser(subparsers):
        subparsers.add_parser(InfoCommand.name, help="Display general info about the current working directory")
        
    def execute(args):       
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
        
