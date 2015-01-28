from collections import namedtuple


Conn = namedtuple('Conn', 'cable,plug')


def connect(recieving, recieving_j, dest, dest_j):
    recieving.connections[recieving_j].append(
        Conn(dest, dest_j)
    )


class Connectable():
    def __init__(self, name):
        self.name = name
        self.reset_state()
        self.reset_connections()

    def reset_connections(self):
        self.connections = {
            k: []
            for k in self.valid_outputs + self.valid_inputs
        }

    def reset_state(self):
        self.state = dict.fromkeys(
            self.valid_inputs + self.valid_outputs,
            0
        )

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

    def set_plug(self, plug, state):
        for conn in self.connections[plug]:
            conn.cable.set_plug(conn.plug, state)

        self.state[plug] = state

    def __repr__(self):
        return '<{}[{}] {} {} {}>'.format(
            self.__class__.__name__,
            self.name,
            self.valid_inputs,
            self.valid_outputs,
            self.state
        )
