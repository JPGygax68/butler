from ..scaffold import Scaffold


class TestCommand:

    name = 'test-scaffolding'
    
    def define_subparser(subparsers):
    
        sp = subparsers.add_parser(TestCommand.name, help='*** for development only ***')
        #sp.add_argument('blabla')
        
    def execute(args):
        s = Scaffold('CMakeLists.txt')
        s.scan_content()


    
    