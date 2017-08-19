
class IndentedTextParser:

    def __init__(self):
        pass
        
    def parse_string(self, text):
        return self.parse_lines([_.rstrip() for _ in text.split("\n")])
            
    # Parses a text file based on line indentation.
    #
    # yields:
    #   ( 1, <parent_branch>)   "entering the content of this parent branch"
    #   (-1, <parent_branch>)   "leaving the content of this parent branch"
    #   (0, <current_branch)    "this is the current branch or leaf"
    #
    # Branches are represented as lists of strings, highest level first.
    #
    # Notes:
    # - no (-1, ...) value is yielded for the end of the lines iterable
    # - indentation is determined by counting the number of leading whitespace characters,
    #   without taking the characters themselves into consideration
    #
    
    def parse_lines(self, lines):
        """Extracts the list of dependencies from the output of "conan info ." (supplied as a string)."""
        reqs = []
        # TODO: the following traversal algorithm could be generalized
        branch = [None]
        indents = [0]
        for line in lines:
            #print(">", line)
            data = line.lstrip()
            indent = len(line) - len(data)
            if indent > indents[-1]:
                yield (1, branch)       # meaning: "enter the content of this parent node"
                branch.append(data)
                indents.append(indent)
            elif indent < indents[-1]:
                while indent < indents[-1]:
                    branch.pop()
                    indents.pop()
                    yield (-1, branch)  # meaning: "exiting this parent node"
            branch[-1] = data
            yield (0, branch)
