import unittest
#import pkgutil
import pkg_resources
from . import Scaffold


#print("Testing the Scaffold class ... NOT YET!")

class TestScaffoldClass(unittest.TestCase):
    
    def test_scan_stream(self):
    
        size = len(pkg_resources.resource_string(__name__, 'testdata/CMakeLists.txt'))
        print("File size:", size)
        
        bs = pkg_resources.resource_stream(__name__, 'testdata/CMakeLists.txt')
        scaffold = Scaffold.from_byte_stream(bs)
        bs.close()
        
        root_node = scaffold.root_node
        self.assertTrue(root_node.depth() == 2)
        print('Root node size:', scaffold.root_node.size())
        self.assertTrue(root_node.size() == size)