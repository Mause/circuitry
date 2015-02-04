import unittest
from itertools import permutations

from ..utils import get_graph, build_pins

multiplexor_cir = get_graph('alu\multiplexor.cir')

multiplexor = multiplexor_cir.get('multiplexor')
multiplexor4_selector = multiplexor_cir.get('multiplexor4_selector')
multiplexor4 = multiplexor_cir.get('multiplexor4')
multiplexor_1bit = multiplexor_cir.get('multiplexor_1bit')
multiplexor_2bits = multiplexor_cir.get('multiplexor_2bits')


TEMPLATE_1BIT = '''\


self[s1] -> [a]({and1.state[a]}) -|
                    |- [o]({and1.state[o]}) -> self[o]
self[a] ->  [b]({and1.state[b]}) -|

self[s1] -> not1[a]({not1.state[a]}) - not1[o]({not1.state[o]}) -> [a]({and2.state[a]}) -|
                                               |- [o]({and2.state[o]}) -> self[o]
self[b] ->                             [b]({and2.state[b]}) -|
'''


def render_1bit(m1):
    print(
        TEMPLATE_1BIT.format_map(m1.graph)
    )


class TestMultiplexor(unittest.TestCase):
    def test_building(self):
        multiplexor('m1')

    def test_lines_zero(self):
        m1 = multiplexor('m1')

        self.assertEqual(m1.get_outputs(), (0,) * 8)

        m1.set_plug('s1', 1)

        self.assertEqual(m1.get_outputs(), (0,) * 8)

        m1.set_plug('s1', 0)

        self.assertEqual(m1.get_outputs(), (0,) * 8)

    def test_operation(self):
        m1 = multiplexor('m1').live()

        self.assertEqual(m1.get_outputs(), (0,) * 8)

        m1.set_plugs(**build_pins(1, (0, 1) * 4))
        m1.set_plugs(**build_pins(2, (1, 0) * 4))

        self.assertEqual(m1.get_outputs(), (1, 0) * 4)

        m1.set_plug('s1', 1)

        self.assertEqual(m1.get_outputs(), (0, 1) * 4)

    def test_1bit(self):
        m1 = multiplexor_1bit('m1').live()

        m1.set_plugs(a=0, b=0, s1=0)
        self.assertEqual(m1.get_outputs(), (0,))
        m1.set_plugs(s1=1)
        self.assertEqual(m1.get_outputs(), (0,))

        # make sure /something/ gets through
        m1.set_plugs(a=1, b=1)
        self.assertEqual(m1.get_outputs(), (1,))

        m1.set_plugs(a=0, b=1, s1=0)
        self.assertEqual(m1.get_outputs(), (1,))  # b selected

        m1.set_plugs(s1=1)
        self.assertEqual(m1.get_outputs(), (0,))  # a selected

        m1.set_plugs(a=1, b=0)
        self.assertEqual(m1.get_outputs(), (1,))  # a still selected

        m1.set_plugs(s1=0)
        self.assertEqual(m1.get_outputs(), (0,))  # b selected

    def test_2bits(self):
        m1 = multiplexor_2bits('m1').live()

        m1.set_plugs(a1=0, b1=0, a2=0, b2=0, s1=0)
        self.assertEqual(m1.get_outputs(), (0, 0))
        m1.set_plugs(s1=1)
        self.assertEqual(m1.get_outputs(), (0, 0))

        # make sure /something/ gets through
        m1.set_plugs(a1=1, b1=1, a2=1, b2=1)
        self.assertEqual(m1.get_outputs(), (1, 1))
        m1.set_plugs(s1=1)
        self.assertEqual(m1.get_outputs(), (1, 1))

        options = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for (a1_val, b1_val), (a2_val, b2_val) in permutations(options, 2):
            for s1_val in [0, 1]:
                m1.set_plugs(s1=s1_val)
                m1.set_plugs(a1=a1_val, b1=b1_val, a2=a2_val, b2=b2_val)

                if s1_val == 1:
                    # a is selected
                    self.assertEqual(
                        m1.get_outputs(),
                        (a1_val, b1_val)
                    )
                else:
                    self.assertEqual(
                        m1.get_outputs(),
                        (a2_val, b2_val)
                    )

    def test_multiplexor4_selector(self):
        sel = multiplexor4_selector('sel').live()
        sel.reset_state()

        sel.set_plugs(s1=1, s2=1)

        sel.set_plugs(s1=0, s2=0)
        self.assertEqual(sel.get_outputs(), (0, 0, 0))

        sel.set_plugs(s1=1, s2=0)
        self.assertEqual(sel.get_outputs(), (0, 1, 0))

        sel.set_plugs(s1=0, s2=1)
        self.assertEqual(sel.get_outputs(), (1, 0, 0))

        sel.set_plugs(s1=1, s2=1)
        self.assertEqual(sel.get_outputs(), (1, 0, 1))

    def test_multiplexor4(self):
        multiplexor4('m4').live()

if __name__ == '__main__':
    unittest.main()
