from collections import UserDict

from .connectable_registry import ConnectableRegistry
from .graph_parser_pp import parse as parse_pp
from .exceptions import NoSuchComponentInScope

import pyparsing


class Graph():
    '''
    This is the external interface for the entire program.

    @param component: the root level customcomponent.
    '''

    def __init__(self, connector=None, customcomponent=None,
                 componentdeclaration=None):
        self.connector = connector or []
        self.customcomponent = customcomponent or []
        self.d_customcomponent = {c.ttype: c for c in self.customcomponent}
        self.componentdeclaration = componentdeclaration or []

    def get_custom(self, ttype):
        return self.d_customcomponent.get(ttype)

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


class LivingGraph(UserDict):
    @property
    def graph(self):
        return self

    def live(self):
        return self.graph.live()


def build_graph(componentdeclaration, connector, base=None):
    graph = (base or {})  # a dict of top level components

    for item in componentdeclaration:
        graph[item.name] = item.resolve_implementation()

    for conn in connector:
        if conn.to_ not in graph:
            raise NoSuchComponentInScope(conn.to_, conn.pos)

        elif conn.from_ not in graph:
            raise NoSuchComponentInScope(conn.from_, conn.pos)

        graph[conn.from_].connect(
            conn.from_,
            conn.from_jack, conn.to_jack, graph[conn.to_]
        )

    return LivingGraph(graph)


def classify_component(thing):
    return thing.__class__.mro()[-2].__name__.lower()


def sort_graph(lst):
    d = {
        'customcomponent': [], 'componentdeclaration': [], 'connector': [],
        'importfile': []
    }

    for thing in lst:
        klass = classify_component(thing)

        if klass in d:
            d[klass].append(thing)

        else:
            raise Exception(classify_component(thing))

    return d


def load_graph(*, filename, graph=None):
    assert filename

    if not graph:
        with open(filename) as fh:
            graph = fh.read()

    try:
        q = parse_pp(graph)
    except pyparsing.ParseException as e:
        raise pyparsing.ParseException(
            pstr=e.pstr,
            loc=e.loc,
            msg='{} in file {}'.format(e.msg, filename),
            elem=e.parserElement
        ) from None

    top_level = sort_graph(q)

    for cus_comp in top_level['customcomponent']:
        cus_comp.graph = sort_graph(cus_comp.contents)
        # this line severly cripples the import mechanism, by making every
        # component loaded essentially global
        ConnectableRegistry.register(cus_comp)

    return Graph(**top_level)

