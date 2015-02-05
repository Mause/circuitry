import unittest
from itertools import product, tee

from circuitry.util import as_bin, from_bin, get_test_graph, build_pins

adder_cir = get_test_graph('alu/adder.cir')
HalfAdder = adder_cir.get('half_adder')
FullAdder = adder_cir.get('full_adder')
EightBitAdder = adder_cir.get('eight_bit_adder')


def half(a, b):
    return HalfAdder('ha').set_plugs(a=a, b=b).get_outputs()


def full(a, b, cin):
    return FullAdder('adder').set_plugs(a=a, b=b, cin=cin).get_outputs()[::-1]





class TestAdder(unittest.TestCase):
    def test_half_adder(self):
        self.assertEqual(half(0, 0), (0, 0))
        self.assertEqual(half(1, 1), (1, 0))
        self.assertEqual(half(1, 0), (0, 1))
        self.assertEqual(half(0, 1), (0, 1))

    def test_full_adder(self):
        self.assertEqual(full(0, 0, 0), (0, 0))
        self.assertEqual(full(0, 0, 1), (0, 1))
        self.assertEqual(full(0, 1, 0), (0, 1))
        self.assertEqual(full(1, 0, 0), (0, 1))
        self.assertEqual(full(1, 1, 0), (1, 0))
        self.assertEqual(full(1, 1, 1), (1, 1))
        self.assertEqual(full(0, 1, 1), (1, 0))
        self.assertEqual(full(1, 0, 1), (1, 0))



if __name__ == '__main__':
    unittest.main()
