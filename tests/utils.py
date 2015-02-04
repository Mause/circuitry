from os.path import dirname, join

from circuitry.graph import load_graph
from circuitry.connectable_impls import CustomComponentImplementation

HERE = dirname(__file__)
ALPHA_8BIT = 'abcdefgh'


class TypeGetter:
    def __init__(self, graph):
        self.graph = graph

    def get(self, ttype):
        component = self.graph.get_custom(ttype)
        if not component:
            raise KeyError('No such component as "{}"'.format(ttype))

        return lambda name: CustomComponentImplementation(name, component, [])


def get_graph(filename):
    return TypeGetter(load_graph(filename=join(HERE, filename)))


def get_custom_component(filename, ttype):
    return get_graph(filename).get(ttype)


def build_pins(num, binary):
    pins = ['{}{}'.format(l, num) for l in ALPHA_8BIT]

    return dict(zip(pins, binary))
