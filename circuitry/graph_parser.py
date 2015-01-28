from string import ascii_letters, digits

from connectable_impls import CustomComponent, ComponentDeclaration
from connector import Cable
from util import PopableWrapper

VALID_IDENT = ascii_letters + digits + '_'


def get_pos(string):
    pos = string.idx
    preceding = string.string[:pos]

    line = preceding.count('\n') + 1
    column = preceding.rfind('\n')
    if column == -1:
        column = pos + 1
    else:
        column = pos - column - 1

    return (line, column)


def expect(string, expected):
    actual = string.read(len(expected))

    if actual == expected:
        return

    line, column = get_pos(string)
    msg = 'Expected "{}", found "{}" at line {}, column {}'.format(
        expected, actual, line, column
    )

    raise Exception(msg)


def whitespace(string):
    while string.peek().isspace() and string.peek():
        string.step()


def parse_ident(string):
    s = []

    while string.peek() in VALID_IDENT:
        s.append(string.pop())

    return ''.join(s)


def parse_ident_list(string):
    expect(string, '[')
    s = []

    while True:
        bit = parse_ident(string)
        if not bit:
            break

        s.append(bit)

        if string.peek() != ']':
            expect(string, ',')

        whitespace(string)

    expect(string, ']')
    return s


def parse_custom_component(string):
    expect(string, '<')
    name = parse_ident(string)
    whitespace(string)
    inputs = parse_ident_list(string)
    whitespace(string)
    outputs = parse_ident_list(string)
    whitespace(string)

    expect(string, '>')
    whitespace(string)
    expect(string, '{')

    contents = parse_(string)

    return CustomComponent(name, inputs, outputs, contents)


def parse_component_definition(string):
    expect(string, '[')

    if string.peek() == '[':
        # we have a list of idents; many component of the same ttype
        name = parse_ident_list(string)

    else:
        name = parse_ident(string)

    whitespace(string)
    ttype = parse_ident(string)
    assert name and ttype, (name, ttype)
    expect(string, ']')

    if isinstance(name, list):
        return [
            ComponentDeclaration(sub_name, ttype)
            for sub_name in name
        ]
    else:
        return [ComponentDeclaration(name, ttype)]


def parse_connection_end(string):
    end = parse_ident(string)
    whitespace(string)
    expect(string, '[')
    whitespace(string)
    jack = parse_ident(string)
    whitespace(string)
    expect(string, ']')
    whitespace(string)

    assert end and jack, (end, jack)

    return end, jack


def parse_connection(string):
    from_, from_jack = parse_connection_end(string)

    whitespace(string)
    expect(string, '->')
    whitespace(string)

    to_, to_jack = parse_connection_end(string)

    return Cable(from_, from_jack, to_, to_jack)


def parse_comment(string):
    while string.peek() != '\n' and not string.at_end():
        string.pop()


def parse_(string, root=False):
    nodes = []

    whitespace(string)
    while string:
        token = string.peek()
        if not token:
            break

        if token == '<':
            if not root:
                raise Exception(
                    'Custom component can only exist at the root level'
                )
            nodes.append(parse_custom_component(string))

        elif token == '[':
            nodes.extend(parse_component_definition(string))

        elif token == '}':
            if root:
                raise Exception('Invalid syntax')
            string.pop()
            return nodes

        elif token == '#':
            parse_comment(string)

        elif token in ascii_letters:
            nodes.append(parse_connection(string))

        whitespace(string)

    return nodes


def parse(string):
    string = PopableWrapper(string)

    return list(parse_(string, root=True))
