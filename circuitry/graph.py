from itertools import groupby

from .connectable_registry import ConnectableRegistry
from .graph_parser import parse


class Graph():
    def __init__(self, connector=None, customcomponent=None,
                 componentdeclaration=None):
        self.connector = connector or []
        self.customcomponent = customcomponent or []
        self.componentdeclaration = componentdeclaration or []

    def __repr__(self):
        return (
            '<Graph connectors={} customcomponents={} componentdeclaration={}>'
            .format(
                len(self.connector),
                len(self.customcomponent),
                len(self.componentdeclaration)
            )
        )

    def build_instance(self):
        return build_graph(
            self.componentdeclaration,
            self.connector
        )


def not_in_graph(name, pos):
    print(pos, ...)
    raise Exception(
        'No such component in scope as "{}". '
        'line {}, column {}'
        .format(name, pos.line, pos.column)
    )


def build_graph(componentdeclaration, connector, base=None):
    graph = (base or {})  # a dict of top level components

    for item in componentdeclaration:
        graph[item.name] = item.resolve_implementation()

    for conn in connector:
        if conn.to_ not in graph:
            not_in_graph(conn.to_, conn.pos)

        elif conn.from_ not in graph:
            not_in_graph(conn.from_, conn.pos)

        graph[conn.from_].connect(
            conn.from_,
            conn.from_jack, conn.to_jack, graph[conn.to_]
        )

    return graph


def classify_component(thing):
    return thing.__class__.mro()[-2].__name__.lower()


def sort_graph(lst):
    return {
        k: list(v)
        for k, v in groupby(lst, key=classify_component)
    }


def load_graph(graph):
    top_level = sort_graph(parse(graph))

    for cus_comp in top_level['customcomponent']:
        cus_comp.graph = sort_graph(cus_comp.contents)
        ConnectableRegistry.register(cus_comp)

    return Graph(**top_level)

get_pin = 'pin{}'.format


def render_header(header):
    return ''.join(map(
        str,
        (
            header.state[get_pin(i)]
            for i in range(8)
        )
    ))


def get_inst():
    with open('sample_graph.txt') as fh:
        raw_graph = fh.read()

    return load_graph(raw_graph).build_instance()


def render_state(state):
    return ' '.join(
        '{}:{}'.format(k, v)
        for k, v in sorted(state.items())
    )


def render_external_state(inst):
    print(
        render_header(inst['input1']), '+',
        render_header(inst['input2']), '=',
        render_header(inst['output'])
    )


def main():
    inst = get_inst()

    num1, num2 = 255, 255
    bnum1, bnum2 = split(num1), split(num2)

    for i in range(8):
        pin = get_pin(i)

        # import pdb
        # pdb.set_trace()
        inst['input1'].set_plug(pin, bnum1[i], False)
        render_external_state(inst)
        inst['input2'].set_plug(pin, bnum2[i], False)
        render_external_state(inst)

    for i in range(1, 9):
        key = 'adder{}'.format(i)
        values = render_state(inst[key].state)
        print('{}: {}'.format(key, values))

    # values =
    print(render_state(inst['output'].state))


    # print(values)
    # assert len(values) == 8

    # value = rejoin(values)
    # print('{} + {} = {}'.format(num1, num2, value))


if __name__ == '__main__':
    main()
