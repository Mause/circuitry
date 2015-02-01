from .graph import load_graph


def render_header(header):
    return ''.join(map(
        str,
        (
            header.get_pin(i)
            for i in range(header.bits)
        )
    ))


def get_inst():
    with open('sample_graph.cir') as fh:
        return load_graph(fh.read()).build_instance()


def render_state(state):
    return ' '.join(
        '{}:{}'.format(k, v)
        for k, v in sorted(state.items())
    )


def render_external_state(inst):
    in1, in2, out = (
        render_header(inst['input1']),
        render_header(inst['input2']),
        render_header(inst['output'])
    )

    print(
        in1, '+', in2, '=', out, '|',
        int(in1, 2), '+', int(in2, 2), '=', int(out, 2)
    )
    input()


def main():
    inst = get_inst()

    # num1, num2 = 255, 255
    # bnum1, bnum2 = split(num1), split(num2)

    from itertools import product

    for a, b in product(range(10), range(10)):
        inst['input1'].set_num(a)
        inst['input2'].set_num(b)

        assert (a + b) == inst['output'].get_num()

        # render_external_state(inst)

    # for i in range(1, 9):
    #     key = 'adder{}'.format(i)
    #     values = render_state(inst[key].state)
    #     print('{}: {}'.format(key, values))

    # print(render_state(inst['output'].state))


if __name__ == '__main__':
    main()
