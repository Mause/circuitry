import unittest

from graph import load_graph
from connectable_impls import CustomComponentImplementation

with open('sample_graph.txt') as fh:
    SAMPLE_GRAPH = load_graph(fh.read())

customcomponent = {t.ttype: t for t in SAMPLE_GRAPH.customcomponent}
HALF_ADDER = customcomponent['half_adder']
FULL_ADDER = customcomponent['full_adder']


def sub_test_half_adder(a, b):
    half_adder = CustomComponentImplementation('ha', HALF_ADDER)
    half_adder.set_plug('a', a)
    half_adder.set_plug('b', b)
    return half_adder.state['c'], half_adder.state['s']


def sub_test_full_adder(a, b, cin):
    adder = CustomComponentImplementation('adder', FULL_ADDER)
    adder.set_plug('a', a)
    adder.set_plug('b', b)
    adder.set_plug('cin', cin)
    return adder.state['cout'], adder.state['s']


wrapper = lambda test_func: lambda self, args, expected: \
    self.assertEqual(test_func(*args), expected)


class TestAdder(unittest.TestCase):
    half = wrapper(sub_test_half_adder)
    full = wrapper(sub_test_full_adder)

    def test_half_adder(self):
        self.half((0, 0), (0, 0))
        self.half((1, 1), (1, 0))
        self.half((1, 0), (0, 1))
        self.half((0, 1), (0, 1))

    def test_full_adder(self):
        self.full((0, 0, 0), (0, 0))
        self.full((1, 0, 0), (0, 1))
        self.full((0, 1, 0), (0, 1))
        self.full((1, 1, 0), (1, 0))
        self.full((0, 0, 1), (0, 1))
        self.full((1, 1, 1), (1, 1))

        self.full((1, 0, 1), (1, 0))
        self.full((0, 1, 1), (1, 0))


if __name__ == '__main__':
    unittest.main()
