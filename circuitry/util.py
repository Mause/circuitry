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


class StateDict(UserDict):
    def __setitem__(self, name, val):
        assert val in {0, 1}
        super().__setitem__(name, val)
