
class IndentedTextParser:

    def __init__(self):
        pass
        
    # TODO: variant that takes iterable of lines
    #
    def parse_string(self, text):
        """Extracts the list of dependencies from the output of "conan info ." (supplied as a string)."""
        reqs = []
        # TODO: the following traversal algorithm could be generalized
        branch = [None]
        indents = [0]
        for line in [_.rstrip() for _ in text.split("\n")]:
            print(">", line)
            data = line.lstrip()
            indent = len(line) - len(data)
            if indent > indents[-1]:
                yield (1, branch)       # meaning: "entering the content of this branch"
                branch.append(data)
                indents.append(indent)
            elif indent < indents[-1]:
                while indent < indents[-1]:
                    branch.pop()
                    indents.pop()
                    yield (-1, branch)  # "leaving the *content* of this branch"
            branch[-1] = data
            yield (0, branch)
            
            #if key == ["PROJECT", "Requires:"]:
            #    yield data
    
