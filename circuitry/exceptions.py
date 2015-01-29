
def render_pos(pos):
    return 'line {}, column {}'.format(pos.line, pos.column)


class CircuitryException(Exception):
    pass


class NoSuchComponentType(CircuitryException):
    def __init__(self, ttype, pos):
        super().__init__(
            'No such component type as "{}". '.format(ttype) +
            render_pos(pos)
        )


class NoSuchComponentInScope(CircuitryException):
    def __init__(self, name, pos):
        super().__init__(
            'No such component in scope as "{}". '.format(name) +
            render_pos(pos)
        )


class GraphSyntaxError(CircuitryException):
    def __init__(self, expected, actual, pos):
        super().__init__(
            'Expected "{}", found "{}" at '.format(expected, actual) +
            render_pos(pos)
        )


class NoSuchPlug(CircuitryException):
    def __init__(self, jack, name, ttype):
        super().__init__(
            'No such plug "{}" on "{}" of type "{}"'
            .format(jack, name, ttype)
        )
