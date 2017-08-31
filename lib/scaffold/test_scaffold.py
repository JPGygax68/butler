import unittest
#import pkgutil
import pkg_resources
from . import Scaffold


class TestScaffoldClass(unittest.TestCase):
    
    def test_basic_parsing(self):
    
        bytes = pkg_resources.resource_string(__name__, 'testdata/cmake1.cmake')
        file_size  = len(bytes)
        rs = pkg_resources.resource_stream(__name__, 'testdata/cmake1.cmake')
        line_count = len([_ for _ in rs])
        rs.close()
        #print("File size in bytes:", file_size)
        #print("File line count   :", line_count)
        
        rs = pkg_resources.resource_stream(__name__, 'testdata/cmake1.cmake')
        scaffold, warnings = Scaffold.from_byte_stream(rs)
        rs.close()
        
        root_node = scaffold.root_node
        self.assertTrue(root_node.depth() == 2)
        
        #print('Root node byte size  :', root_node.byte_size ())
        #print('Root node line count :', root_node.line_count())
        #print('Root node child count:', len(root_node.children))
        self.assertEqual(root_node.byte_size (), file_size)
        self.assertEqual(root_node.line_count(), line_count)
        self.assertEqual(len(root_node.children), 3)
        
        tagged_nodes = [_ for _ in root_node.yield_tagged_children()]
        self.assertEqual(len(tagged_nodes), 1)
        self.assertEqual(tagged_nodes[0].tag(), 'main-target')
        
        content = tagged_nodes[0].content().decode('utf-8')
        self.assertTrue('add_executable' in content)
        
    def test_warnings(self):

        rs = pkg_resources.resource_stream(__name__, 'testdata/cmake2.cmake')
        scaffold, warnings = Scaffold.from_byte_stream(rs)
        rs.close()
        
        self.assertEqual(len(warnings), 1)
        warning = warnings[0]
        line_num, col_num = warning[0]
        message = warning[1]
        self.assertEqual(line_num, 19)
        self.assertEqual(col_num, 4)
        self.assertIn('indent mismatch', message)
     
    def test_finding_nodes_by_type(self):

        rs = pkg_resources.resource_stream(__name__, 'testdata/cmake1.cmake')
        scaffold, warnings = Scaffold.from_byte_stream(rs)
        rs.close()
        
        main_target = scaffold.find_nodes_by_type('main-target')[0]
        
        self.assertIn('add_executable', main_target.content().decode('utf-8'))
        
        
    #def test_appending(self):
    #    
    #    rs = pkg_resources.resource_stream(__name__, 'testdata/cmake2.txt')
    #    scaffold, warnings = Scaffold.from_byte_stream(rs)
    #    rs.close()
    #    
    #    # ...
    #    
    #    ref = pkg_resources.resource_string(__name__, 'testdata/cmake3.txt')
        