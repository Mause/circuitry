import string
from collections import namedtuple

from pyparsing import (
    Word, alphas, Literal, Forward, ZeroOrMore, delimitedList, restOfLine,
    Optional
)

from .connector import Cable
from . import connectable_impls
from .util import get_pos


class ImportFile:
    def __init__(self, filename, components):
        self.filename = filename
        self.components = components

    def __repr__(self):
        return '<Import [{}] from {}>'.format(
            ','.join(self.components), self.filename
        )


def build_declaration(s, loc, tok):
    return [
        connectable_impls.ComponentDeclaration(
            name, tok.ttype, get_pos(loc, s), []
        )
        for name in tok[:-1]
    ]


def build_component(instring, loc, tok):
    return connectable_impls.CustomComponent(
        tok['name'],
        list(tok['inputs']),   # stop pyparsing from leaking out
        list(tok['outputs']),  # stop pyparsing from leaking out
        tok.get('contents', [])[1:-1]
    )


def build_cable(instring, loc, tok):
    from_, from_jack = tok[0].name, tok[0].jacks
    to_, to_jack = tok[2].name, tok[2].jacks

    assert len(from_jack) == len(to_jack)

    pos = get_pos(loc, instring)
    return [
        Cable(from_, sub_from_jack, to_, sub_to_jack, pos)
        for sub_from_jack, sub_to_jack in zip(from_jack, to_jack)
    ]


End = namedtuple('End', 'name,jacks')
OPEN = Literal('[').addParseAction(lambda: [])
CLOSE = Literal(']').addParseAction(lambda: [])
WORD = Word(alphas + string.digits + '_').setName('WORD')
TType = Word(alphas + string.digits + '_.').setName('ttype')
LT = Literal('<')
GT = Literal('>')
OPEN_C = Literal('{')
CLOSE_C = Literal('}')

IdentList = OPEN + Optional(delimitedList(WORD)) + CLOSE
WordOrWords = IdentList() | WORD
WordOrWords.setName('WordOrWords')

ConnectorEnd = TType + OPEN + WordOrWords() + CLOSE
ConnectorEnd.addParseAction(lambda tok: End(tok[0], tok[1:]))
Connector = ConnectorEnd() + Literal('->') + ConnectorEnd()
Connector.setName('Connector')
Connector.addParseAction(build_cable)

Grammar = Forward()

CustomComponentHeader = (
    LT + WORD('name') + IdentList('inputs') + IdentList('outputs') + GT
)
CustomComponentBody = OPEN_C + ZeroOrMore(Grammar('contents')) + CLOSE_C
CustomComponent = CustomComponentHeader + CustomComponentBody('contents')
CustomComponent.addParseAction(build_component)


ComponentDeclarationComponents = WordOrWords()
ComponentDeclaration = (
    OPEN + ComponentDeclarationComponents('components') + WORD('ttype') + CLOSE
)
ComponentDeclaration.setName('ComponentDeclaration')
ComponentDeclaration.addParseAction(build_declaration)

Import = (
    Literal('@import') +
    WordOrWords + Literal('from') + WORD('filename') +
    Literal('@')
)
Import.addParseAction(lambda tok: ImportFile(tok.filename, tok[1:-3]))


SubGrammar = ComponentDeclaration | Connector | Import | CustomComponent
Grammar <<= (SubGrammar + Grammar) | SubGrammar
Grammar.setName('Grammar')

Header = (
    OPEN +
    WORD('filename').setName('filename') +
    WordOrWords('inputs') + WordOrWords('outputs') +
    CLOSE
)

Header.addParseAction(
    lambda tok: (
        tok.filename,
        tok.inputs,
        tok.outputs
    )
)


def build_file(tok):
    return tok[1:]
    # filename, inputs, outputs = tok[0]

    # from .graph import Graph
    # return Graph(
    #     connectable_impls.CustomComponent(
    #         filename,
    #         inputs, outputs,
    #         tok[1]
    #     )
    # )


File = Header + Grammar
File.addParseAction(build_file)
Comment = '#' + restOfLine
File.ignore(Comment)


def parse(string):
    return File.parseString(string, parseAll=True).asList()


def main():
    with open('sample_graph.cir') as fh:
        from pprint import pprint

        pprint(parse(fh.read()))

if __name__ == '__main__':
    main()
