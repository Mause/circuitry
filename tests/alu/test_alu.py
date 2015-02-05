import unittest

from circuitry.util import get_test_graph

alu_cir = get_test_graph('alu/alu.cir')
alu = alu_cir.get('alu')

subtractor_cir = get_graph('alu/subtractor.cir')
subtractor_1bit = subtractor_cir.get('subtractor_1bit')
# negator = alu_cir.get('negator')


class TestALU(unittest.TestCase):
    def test_initalisation(self):
        alu('alu')

    def test_adding(self):
        a1 = alu('a1')

        a1.set_plug('s1', 0)
        a1.set_plug('s1', 1)
        a1.set_plug('s1', 0)

        self.assertEqual(a1.get_outputs(), (0,) * 9)
        a1.set_plug('s1', 1)
        self.assertEqual(a1.get_outputs(), (0,) * 9)

        a1.set_plug('a1', 1)

        self.assertEqual(a1.get_outputs(), (0,) * 7 + (1, 0))
        a1.set_plug('s1', 0)
        self.assertEqual(a1.get_outputs(), (0,) * 9)

    def test_anding(self):
        a1 = alu('a1').live()

        a1.set_plug('s1', 0)
        a1.set_plug('s1', 1)
        a1.set_plug('s1', 0)

        a1.set_plugs()

    def test_subtractor_1bit(self):
        s1 = subtractor_1bit('s1')

        s1.set_plugs()

    # def test_negator(self):
    #     n1 = negator('n1')

    #     n1.set_plugs(**build_pins(1, (1,) * 8))
    #     n1.set_plugs(**build_pins(1, (0,) * 8))
    #     n1.set_plug('sign1', 0)

    #     for a in range(254):
    #         print(a)
    #         b = as_bin(a)[::-1]
    #         n1.set_plugs(**build_pins(1, b))
    #         # for thing in sorted(n1.graph.graph):
    #         #     print(thing, n1.graph.graph[thing].state)
    #         # print(n1.get_outputs())
    #         o = n1.get_outputs()[::-1]
    #         print(b, o)
    #         self.assertEqual(from_bin(o), -a)

if __name__ == '__main__':
    unittest.main()
