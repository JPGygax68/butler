import re


#_splitter = re.compile(r'^\s*#\$\:\s*(\w+)\s*(?:\:(.*))?$((?:\n.*$)*)\n^\s*#\$/\s*(\1)(?:.*)$', re.MULTILINE)
#        
#def _scan_string(s):
#    for m in _splitter.finditer(s):
#        print('--------------------------------')
#        print(m.group(3))


class Node:
    def __init__(self, byte_count = 0, line_count = 0):
        self.type = type
        self.byte_count = byte_count
        self.line_count = line_count
        self.children = []
        
    def append(self, bytes, lines):
        assert not (bytes == 0 and lines != 0)
        if self.children:
            assert self.children[-1].is_sealed()
            self.children.append( Node() )
            self.children[-1].append(bytes, lines)
        else:
            self.byte_count += bytes
            self.line_count += lines
        
    def create_new_branch(self):
        print(">create_new_branch()")
        # No branches yet (was a leaf) ?
        if not self.children:
            child = Node(self.byte_count, self.line_count)
            self.byte_count = self.line_count = 0
            self.children = [child]
        else:
            if not self.children[-1].is_sealed():
                self.children[-1].seal()
            child = Node()
            self.children.append(child)
        return child
        
    def seal(self):
        print(">seal()")
        if self.children:
            if self.children[-1].byte_count == 0:
                self.children.pop()
        self._sealed = True
    
    def is_sealed(self):
        return self._sealed
        
    def depth(self):
        print(">depth(), children:", self.children)
        return 1 + (0 if not self.children else max([_.depth() for _ in self.children]))

    def size(self):
        return self.byte_count if not self.children else sum([_.size() for _ in self.children])
        
        
class Scaffold:

    def from_byte_stream(stream, encoding='utf-8'):
    
        sc = Scaffold()
        
        curr_branch = [Node()]
        
        for line_buf in stream:
            line = line_buf.decode(encoding).rstrip()
            if line[:2] == '#$': # TODO: support other comment introducers
                if line[2] == ':':
                    curr_branch[-1].append(len(line_buf), 1)
                    child = curr_branch[-1].create_new_branch()
                    curr_branch.append(child)
                elif line[2] == '/':
                    curr_branch[-1].seal()
                    curr_branch[-1].append(len(line_buf), 1)
            else:
                curr_branch[-1].append(len(line_buf), 1)
        #else:
        #    print('EOF, total size:', byte_offs)
                
        sc.root_node = curr_branch[0]
        sc.root_node.seal()
        
        return sc
