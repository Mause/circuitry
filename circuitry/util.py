from collections import namedtuple, UserDict

Pos = namedtuple('Pos', 'line,column')


def get_pos(pos, instring):
    preceding = instring[:pos]

    line = preceding.count('\n') + 1
    column = preceding.rfind('\n')
    if column == -1:
        column = pos + 1
    else:
        column = pos - column - 1

    return Pos(line, column)


class PopableWrapper():
    def __init__(self, string):
        self.string = string
        self.idx = 0

    def at_end(self):
        return self.idx == (len(self.string) - 1)

    def step(self, n=1):
        if (self.idx + n) <= len(self.string):
            self.idx += n

    def pop(self):
        char = self.peek()
        self.step()
        return char

    def peek(self):
        return self.string[self.idx:self.idx+1]

    def read(self, n):
        chars = self.string[self.idx:self.idx + n]
        self.idx += n
        return chars

    def __repr__(self):
        return '<PopableWrapper {}>'.format(repr(self.string[self.idx:]))


class StateDict(UserDict):
    def __setitem__(self, name, val):
        assert val in {0, 1}
        super().__setitem__(name, val)
