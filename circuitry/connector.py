

class Connector():
    def __init__(self):
        ...


class Cable(Connector):
    def __init__(self, from_, from_jack, to_, to_jack,
                 custom_component_connection):
        self.from_ = from_
        self.from_jack = from_jack
        self.to_ = to_
        self.to_jack = to_jack
        self.custom_component_connection = custom_component_connection
        super().__init__()

    def __repr__(self):
        return '<Cable {}[{}] -> {}[{}]>'.format(
            self.from_,
            self.from_jack,
            self.to_,
            self.to_jack
        )
