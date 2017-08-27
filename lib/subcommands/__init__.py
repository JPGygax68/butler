# Subcommands

# TODO: use instantiated subcommand objects instead of class methods


from .info_cmd import InfoCommand
from .removesubmodule_cmd import RemoveSubmoduleCommand
from .test_cmd import TestCommand


subcommands = [
    InfoCommand, 
    RemoveSubmoduleCommand,
    TestCommand
]