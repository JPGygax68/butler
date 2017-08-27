import git
#from grips import GitGrip


class RemoveSubmoduleCommand:

    sp = None
    
    def define_subparser(subparsers):
    
        sp = subparsers.add_parser('remove-submodule')
        sp.add_argument('submodule')

    def remove_submodule(ns):
        repo = git.Repo('.')
        matches = [_ for _ in repo.submodules if _._name == args.submodule]
        if not matches: raise Exception('Submodule %s does not exist' % args.submodule)
        sm = matches.next()
        sm.remove()
        print('Submodule %s successfully removed')
