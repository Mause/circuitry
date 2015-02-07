import argparse
from functools import reduce

from circuitry.util import get_test_graph, build_pins, as_bin, from_bin

adder_cir = get_test_graph('alu\\adder.cir')
sixteen_bit_adder = adder_cir.get('sixteen_bit_adder')


def main():
    inst = sixteen_bit_adder('inst').live()

    def set_plugs(i, d):
        pins = build_pins(i, as_bin(d, 16))
        assert len(pins) <= 16, (
            'Only supports up to sixteen bit numbers thus far'
        )
        inst.set_plugs(**pins)

    def add(a, b):
        set_plugs(1, a)
        set_plugs(2, b)
        return from_bin(inst.get_outputs('abcdefghijklmnop'))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'ints',
        type=int,
        action='append',
        nargs='+'
    )

    ints = parser.parse_args().ints[0]
    print(reduce(add, ints))


if __name__ == '__main__':
    main()
