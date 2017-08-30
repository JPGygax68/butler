import re


#_splitter = re.compile(r'^\s*#\$\:\s*(\w+)\s*(?:\:(.*))?$((?:\n.*$)*)\n^\s*#\$/\s*(\1)(?:.*)$', re.MULTILINE)
#        
#def _scan_string(s):
#    for m in _splitter.finditer(s):
#        print('--------------------------------')
#        print(m.group(3))


class Node:
    def __init__(self, tag = None, _byte_count = 0, _line_count = 0):
        self._tag = tag
        self._byte_count = _byte_count
        self._line_count = _line_count
        self.children = []
        self._sealed = False
        
    def append(self, bytes, lines):
        assert not (bytes == 0 and lines != 0)
        if self.children:
            if self.children[-1].is_sealed():
                self.children.append( Node() )
            self.children[-1].append(bytes, lines)
        else:
            self._byte_count += bytes
            self._line_count += lines
        
    def create_new_branch(self, tag = None):
        #print(">create_new_branch()")
        # No branches yet (was a leaf) ?
        if not self.children:
            child = Node(None, self._byte_count, self._line_count)
            self._byte_count = self._line_count = 0
            self.children = [child]
        else:
            if not self.children[-1].is_sealed():
                self.children[-1].seal()
        child = Node(tag)
        self.children.append(child)
        return child
        
    def seal(self):
        #print(">seal()")
        if self.children:
            if self.children[-1]._byte_count == 0:
                self.children.pop()
        self._sealed = True
    
    def is_tagged(self):
        return not self._tag is None
        
    def tag(self):
        return self._tag
        
    def is_sealed(self):
        return self._sealed
        
    def depth(self):
        #print(">depth(), children:", self.children)
        return 1 + (0 if not self.children else max([_.depth() for _ in self.children]))

    def byte_size(self):
        return self._byte_count if not self.children else sum([_.byte_size() for _ in self.children])

    def line_count(self):
        return self._line_count if not self.children else sum([_.line_count() for _ in self.children])
        
    def yield_tagged_children(self):
        for node in self.children:
            if node.is_tagged():
                yield node
        
        
class Scaffold:

    # TODO: support indented tag lines
    # TODO: warn if indentation of opener and closer differ
    
    def from_byte_stream(stream, encoding='utf-8'):
    
        sc = Scaffold()
        
        curr_branch = [Node()]
        
        for line_buf in stream:
            line = line_buf.decode(encoding).rstrip()
            if line[:2] == '#$': # TODO: support other comment introducers
                # Element openers and closers become part of the *containing* node (for now)
                if line[2] == ':':
                    curr_branch[-1].append(len(line_buf), 1)
                    child = curr_branch[-1].create_new_branch(line[3:].strip())
                    curr_branch.append(child)
                elif line[2] == '/':
                    curr_branch[-1].seal()
                    curr_branch.pop()
                    curr_branch[-1].append(len(line_buf), 1)
            else:
                curr_branch[-1].append(len(line_buf), 1)
        #else:
        #    print('EOF, total byte_size:', byte_offs)
                
        sc.root_node = curr_branch[0]
        sc.root_node.seal()
        
        return sc
