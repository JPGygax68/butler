import re


class Scaffold:

    def __init__(self, filename):
    
        with open(filename, 'r') as f:
            self.content = f.read()
        #print(self.content)
        
        p = re.compile(r'^\s*#\$\:\s*(\w+)\s*(?:\:(.*))?$((?:\n.*$)*)\n^\s*#\$/\s*(\1)(?:.*)$', re.MULTILINE)
        for m in p.finditer(self.content):
            print('Opener:', m.group(1), m.group(2))
            print(m.group(3))
            print("Closer:", m.group(4))
        
        
        