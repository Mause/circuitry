from collections import namedtuple

from .util import StateDict
from .exceptions import NoSuchPlug

Conn = namedtuple('Conn', 'cable,plug')


def connect(recieving, recieving_j, dest, dest_j):
    if recieving_j not in recieving.connections:
        raise NoSuchPlug(recieving_j, recieving.name, recieving.ttype)

    recieving.connections[recieving_j].append(
        Conn(dest, dest_j)
    )


class Connectable():
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.reset_state()
        self.reset_connections()

    @classmethod
    def build(cls, name, args):
        return cls(name, args)

    def reset_connections(self):
        self.connections = {
            k: []
            for k in self.valid_outputs + self.valid_inputs
        }

    def reset_state(self):
        self.state = StateDict.fromkeys(
            self.valid_inputs + self.valid_outputs,
            0
        )

    def get_outputs(self):
        return tuple(self.state[key] for key in self.valid_outputs)

    def get_inputs(self, keys=None):
        keys = keys or self.valid_inputs
        return tuple(self.state[key] for key in keys)

    def render_connect(self, output_j, input_j, cable):
        ...
        # print('{}[{}] -> {}[{}]'.format(
        #     self.name, output_j, cable.name, input_j
        # ))

    def connect(self, ref, output_j, input_j, cable):
        """
        plug is the the name of the input we're connecting the cable to
        """
        connect(self, output_j, cable, input_j)

    def set_plugs(self, **kw):
        for plug, state in kw.items():
            self.set_plug(plug, state)
        return self

    def set_plug(self, plug, state):
        assert state in {0, 1}

        # use a try-except, as this will never happen during normal operation
        try:
            self.connections[plug]
        except KeyError:
            raise NoSuchPlug(
                plug,
                self.name,
                self.ttype
            )

        for conn in self.connections[plug]:
            conn.cable.set_plug(conn.plug, state)

        self.state[plug] = state
        return self

    def __repr__(self):
        return '<{}[{}] {} {} {}>'.format(
            self.__class__.__name__,
            self.name,
            self.valid_inputs,
            self.valid_outputs,
            self.state
        )
