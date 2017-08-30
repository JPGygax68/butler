import unittest
#import pkgutil
import pkg_resources
from . import Scaffold


class TestScaffoldClass(unittest.TestCase):
    
    def test_scan_stream(self):
    
        file_size  = len(pkg_resources.resource_string(__name__, 'testdata/CMakeLists.txt'))
        rs = pkg_resources.resource_stream(__name__, 'testdata/CMakeLists.txt')
        line_count = len([_ for _ in rs])
        rs.close()
        print("File size in bytes:", file_size)
        print("File line count   :", line_count)
        
        bs = pkg_resources.resource_stream(__name__, 'testdata/CMakeLists.txt')
        scaffold = Scaffold.from_byte_stream(bs)
        bs.close()
        
        root_node = scaffold.root_node
        self.assertTrue(root_node.depth() == 2)
        
        print('Root node byte size  :', root_node.byte_size ())
        print('Root node line count :', root_node.line_count())
        print('Root node child count:', len(root_node.children))
        self.assertEqual(root_node.byte_size (), file_size)
        self.assertEqual(root_node.line_count(), line_count)
        self.assertEqual(len(root_node.children), 3)
        
        tagged_nodes = [_ for _ in root_node.yield_tagged_children()]
        self.assertEqual(len(tagged_nodes), 1)
        self.assertEqual(tagged_nodes[0].tag(), 'main-target')