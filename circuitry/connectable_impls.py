import gates
from connectable import Connectable
from connectable_registry import ConnectableRegistry


@ConnectableRegistry.register
class HeaderConnectable(Connectable):
    ttype = 'header'
    valid_plugs = ['pin{}'.format(x) for x in range(8)]
    valid_inputs = valid_outputs = valid_plugs


@ConnectableRegistry.register
class AndConnectable(Connectable):
    ttype = 'and'

    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return self.state['a'] and self.state['b']

    def set_plug(self, plug, state):
        assert plug in self.valid_inputs

        old_state = self.calc_state()

        super().set_plug(plug, state)

        new_state = self.calc_state()
        if new_state != old_state:
            super().set_plug('o', state)


@ConnectableRegistry.register
class XORConnectable(Connectable):
    ttype = 'xor'
    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return gates.xor(self.state['a'], self.state['b'])

    def set_plug(self, plug, state):
        assert plug in self.valid_inputs

        old_state = self.calc_state()

        super().set_plug(plug, state)

        new_state = self.calc_state()
        if old_state != new_state:
            super().set_plug('o', new_state)


@ConnectableRegistry.register
class OrConnectable(Connectable):
    ttype = 'or'
    valid_inputs = ['a', 'b']
    valid_outputs = ['o']

    def calc_state(self):
        return self.state['a'] or self.state['b']

    def set_plug(self, plug, state):
        assert plug in self.valid_inputs

        old_state = self.calc_state()

        super().set_plug(plug, state)

        new_state = self.calc_state()
        if old_state != new_state:
            super().set_plug('o', new_state)


class ComponentDeclaration():
    def __init__(self, name, ttype):
        self.name = name
        self.ttype = ttype

    def resolve_implementation(self):
        impl = ConnectableRegistry.instance().registry[self.ttype]

        if isinstance(impl, CustomComponent):
            return CustomComponentImplementation(self.name, impl)

        else:
            return impl(self.name)


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


class CustomComponentImplementation(Connectable):
    def __init__(self, name, reference):
        self.reference = reference
        super().__init__(name)

        # avoid import loop
        from graph import build_graph
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
