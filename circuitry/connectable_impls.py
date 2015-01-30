
from . import gates
from .connectable import Connectable
from .connectable_registry import ConnectableRegistry
from .exceptions import NoSuchComponentType


@ConnectableRegistry.register
class HeaderConnectable(Connectable):
    ttype = 'header'

    def __init__(self, name, args):
        self.bits = int(args[0]) if args else 8

        self.valid_inputs = self.valid_outputs = [
            self.get_pin_name(x) for x in range(self.bits)
        ]

        super().__init__(name, args)

    @staticmethod
    def get_pin_name(i):
        return 'pin{}'.format(i)

    def get_pin(self, i):
        return self.state[self.get_pin_name(i)]

    def set_pin(self, i, state):
        assert state in {0, 1}
        self.set_plug(self.get_pin_name(i), state)

    def get_num(self):
        bits = map(self.get_pin, range(self.bits))
        bits = map(str, bits)

        return int(''.join(bits), 2)

    def set_num(self, num):
        for i in range(self.bits):
            q = (num >> i) & 1
            assert q in {0, 1}

            self.set_pin(i, q)


class HasDynamicStateMixin:
    def calc_state(self):
        raise NotImplementedError()

    def set_plug(self, plug, state):
        assert plug in self.valid_inputs

        old_state = self.calc_state()

        super().set_plug(plug, state)

        new_state = self.calc_state()
        if old_state != new_state:
            super().set_plug('o', new_state)


@ConnectableRegistry.register
class AndConnectable(HasDynamicStateMixin, Connectable):
    ttype = 'and'

    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return int(self.state['a'] and self.state['b'])


@ConnectableRegistry.register
class XORConnectable(HasDynamicStateMixin, Connectable):
    ttype = 'xor'
    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return int(gates.xor(self.state['a'], self.state['b']))


@ConnectableRegistry.register
class OrConnectable(HasDynamicStateMixin, Connectable):
    ttype = 'or'
    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return int(self.state['a'] or self.state['b'])


@ConnectableRegistry.register
class NotConnectable(HasDynamicStateMixin, Connectable):
    ttype = 'not'
    valid_inputs = ['a']
    valid_outputs = ['o']

    def calc_state(self):
        return int(not self.state['a'])


@ConnectableRegistry.register
class NandConnectable(HasDynamicStateMixin, Connectable):
    ttype = 'nand'
    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        a, b = self.state['a'], self.state['b']

        return int(not (a and b))


class ComponentDeclaration():
    def __init__(self, name, ttype, pos, args):
        self.name = name
        self.ttype = ttype
        self.pos = pos
        self.args = args

    def resolve_implementation(self):
        registry = ConnectableRegistry.instance().registry

        if self.ttype not in registry:
            raise NoSuchComponentType(self.ttype, self.pos)

        return registry[self.ttype].build(self.name, self.args)


class CustomComponent():
    def __init__(self, name, inputs, outputs, contents):
        self.ttype = self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.contents = contents

    def __repr__(self):
        return '<CustomComponent[{}] inputs=[{}] outputs=[{}]>'.format(
            self.name,
            ','.join(self.inputs),
            ','.join(self.outputs)
        )

    def build(self, name, args):
        return CustomComponentImplementation(name, self, args)


class CustomComponentImplementation(Connectable):
    def __init__(self, name, reference, args):
        self.reference = reference
        super().__init__(name, args)

        # avoid import loop
        from .graph import build_graph
        self.graph = build_graph(
            self.reference.graph['componentdeclaration'],
            self.reference.graph['connector'],
            {'self': self}
        )

        assert self.reference.inputs != self.reference.outputs

    @property
    def ttype(self):
        return self.reference.ttype

    valid_inputs = property(lambda self: self.reference.inputs)
    valid_outputs = property(lambda self: self.reference.outputs)

    def __repr__(self):
        # splice the ttype in
        s = super().__repr__()

        first, second = s.split(self.name)

        return '{}{}][{}{}'.format(
            first, self.name, self.ttype, second
        )
