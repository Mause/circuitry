from os.path import join, dirname

from collections import namedtuple

ALPHA_8BIT = 'abcdefgh'
HERE = join(dirname(__file__), '..', 'tests')

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


class TypeGetter:
    def __init__(self, graph):
        self.graph = graph

    def get(self, ttype):
        from circuitry.connectable_impls import CustomComponentImplementation
        component = self.graph.get_custom(ttype)
        if not component:
            raise KeyError('No such component as "{}"'.format(ttype))

        return lambda name: CustomComponentImplementation(name, component, [])


def get_graph(filename):
    from circuitry.graph import load_graph
    return TypeGetter(load_graph(filename=join(HERE, filename)))


def get_custom_component(filename, ttype):
    return get_graph(filename).get(ttype)


class StateDict(UserDict):
    def __setitem__(self, name, val):
        assert val in {0, 1}
        super().__setitem__(name, val)


def build_pins(num, binary):
    pins = ['{}{}'.format(l, num) for l in ALPHA_8BIT]

    return dict(zip(pins, binary))
