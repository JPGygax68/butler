import re


#_splitter = re.compile(r'^\s*#\$\:\s*(\w+)\s*(?:\:(.*))?$((?:\n.*$)*)\n^\s*#\$/\s*(\1)(?:.*)$', re.MULTILINE)
#        
#def _scan_string(s):
#    for m in _splitter.finditer(s):
#        print('--------------------------------')
#        print(m.group(3))


class Node:
    def __init__(self, tag = None, content = b'', line_count = 0):
        self._tag = tag
        self._content = content
        self._line_count = line_count
        self.children = []
        self._sealed = False
        
    def append(self, content, line_count):
        assert not (len(content) == 0) and line_count != 0
        if self.children:
            if self.children[-1].is_sealed():
                self.children.append( Node() )
            self.children[-1].append(content, line_count)
        else:
            self._content += content
            self._line_count += line_count
        
    def create_new_branch(self, tag = None):
        #print(">create_new_branch()")
        # No branches yet (was a leaf) ?
        if not self.children:
            # Transfer content so far to new untagged child
            child = Node(None, self._content, self._line_count)
            self._content = None
            self._line_count = 0
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
            last = self.children[-1]
            if last._content is None or len(last._content) == 0:
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
        return len(self._content) if not self.children else sum([_.byte_size() for _ in self.children])

    def line_count(self):
        return self._line_count if not self.children else sum([_.line_count() for _ in self.children])
        
    def content(self):
        if self.children:
            return b''.join([_.content() for _ in self.children])
        else:
            return self._content
        
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
        indents = []
        
        for line_buf in stream:
            line = line_buf.decode(encoding).rstrip()
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            if line[:2] == '#$': # TODO: support other comment introducers
                # Element openers and closers become part of the *containing* node (for now)
                if line[2] == ':':
                    indents.append(indent)
                    curr_branch[-1].append(line_buf, 1)
                    child = curr_branch[-1].create_new_branch(line[3:].strip())
                    curr_branch.append(child)
                elif line[2] == '/':
                    curr_branch[-1].seal()
                    curr_branch.pop()
                    if indent != indents[-1]:
                        raise Exception('opening/closing tag indent mismatch (opening: %d, closing %d)' % (indents[-1], indent))
                    indents.pop()
                    curr_branch[-1].append(line_buf, 1)
            else:
                curr_branch[-1].append(line_buf, 1)
        #else:
        #    print('EOF, total byte_size:', byte_offs)
                
        sc.root_node = curr_branch[0]
        sc.root_node.seal()
        
        return sc
