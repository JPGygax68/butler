import git
#from grips import GitGrip

# TODO: delegate to the Git grip instead of using the git module directly ?


class RemoveSubmoduleCommand:

    subcommand = 'remove-submodule'
        
    def define_subparser(subparsers):
    
        sp = subparsers.add_parser('remove-submodule', help='Remove a Git submodule')
        sp.add_argument('submodule')

    def execute(args):
        repo = git.Repo('.')
        matches = [_ for _ in repo.submodules if _._name == args.submodule]
        if not matches: raise Exception('Submodule %s does not exist' % args.submodule)
        sm = matches.next()
        sm.remove()
        print('Submodule %s successfully removed')
