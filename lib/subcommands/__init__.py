# Subcommands

# TODO: use instantiated subcommand objects instead of class methods


from .info_cmd import InfoCommand
from .removesubmodule_cmd import RemoveSubmoduleCommand

subcommands = [
    InfoCommand, 
    RemoveSubmoduleCommand
]