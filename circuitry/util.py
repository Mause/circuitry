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


def as_bin(i):
    return tuple(map(int, bin(i)[2:].rjust(8, '0')))


def from_bin(i):
    if len(i) == 9:
        sign, *i = i

    i = int(''.join(map(str, i)), 2)

    return -i if sign else i


class StateDict(UserDict):
    def __setitem__(self, name, val):
        assert val in {0, 1}
        super().__setitem__(name, val)
