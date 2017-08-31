import re


class Node:
    def __init__(self, tag = None, content = b'', line_count = 0):
        self._tag = tag
        self._content = content
        self._line_count = line_count
        self.children = []
        self._sealed = False
        if tag:
            # TODO: also parse attributes
            xp = re.compile(r'^[^\d\W][-\w]*', re.UNICODE)
            m = xp.match(self._tag)
            if m: self._type = m.string
        else:
            self._type = None
        
    def append_content(self, content, line_count):
        assert not (len(content) == 0) and line_count != 0
        if self.children:
            if self.children[-1].is_sealed():
                self.children.append( Node() )
            self.children[-1].append_content(content, line_count)
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
        
    def gather_nodes_by_type(self, node_type):
        if self.node_type() == node_type:
            return [self]
        elif self.children:
            list = []
            for child in self.children:
                list += child.gather_nodes_by_type(node_type)
            return list
        else:
            return []

    def node_type(self):
        return self._type
        

class Scaffold:

    # TODO: support indented tag lines
    # TODO: warn if indentation of opener and closer differ
    
    def from_byte_stream(stream, encoding='utf-8'):
    
        sc = Scaffold()
        
        curr_branch = [Node()]
        indents = []
        warnings = []
        
        line_num = 1
        for line_buf in stream:
            line = line_buf.decode(encoding).rstrip()
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            if line[:2] == '#$': # TODO: support other comment introducers
                # Element openers and closers become part of the *containing* node (for now)
                if line[2] == '[':
                    indents.append(indent)
                    curr_branch[-1].append_content(line_buf, 1)
                    tag = line[3:].strip()
                    child = curr_branch[-1].create_new_branch(tag)
                    curr_branch.append(child)
                elif line[2] == ']': # ignoring the rest of the line (for now)
                    curr_branch[-1].seal()
                    curr_branch.pop()
                    if indent != indents[-1]:
                        #raise Exception('opening/closing tag indent mismatch (opening: %d, closing %d)' % (indents[-1], indent))
                        msg = 'opening/closing tag indent mismatch (opening: %d, closing %d)' % (indents[-1], indent)
                        warnings.append(((line_num, indent), msg))
                    indents.pop()
                    curr_branch[-1].append_content(line_buf, 1)
            else:
                curr_branch[-1].append_content(line_buf, 1)
            line_num += 1
        #else:
        #    print('EOF, total byte_size:', byte_offs)
                
        sc.root_node = curr_branch[0]
        sc.root_node.seal()
        
        return sc, warnings

    def find_nodes_by_type(self, type):
        
        return self.root_node.gather_nodes_by_type(type)