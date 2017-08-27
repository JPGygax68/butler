# "git" grip

import pathlib as pl
import git


class GitGrip:

    def display_info():
        if not pl.Path('.git').is_dir():
            print("This directory is not a (non-bare) git repository")
        else:
            print("Directory is a git repository, obtaining info...")
            repo = git.Repo('.')
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
        
        
    # Command: remove submodule

    def remove_submodule(args):
        repo = git.Repo('.')
        matches = [_ for _ in repo.submodules if _._name == args.submodule]
        if not matches: raise Exception('Submodule %s does not exist' % args.submodule)
        sm = matches.next()
        sm.remove()
        print('Submodule %s successfully removed')
