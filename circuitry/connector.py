

class Connector():
    def __init__(self):
        ...


class Cable(Connector):
    def __init__(self, from_, from_jack, to_, to_jack, pos):
        self.from_ = from_
        self.from_jack = from_jack
        self.to_ = to_
        self.to_jack = to_jack
        self.pos = pos
        super().__init__()

    def __repr__(self):
        return '<Cable {}[{}] -> {}[{}] l{}:c{}>'.format(
            self.from_,
            self.from_jack,
            self.to_,
            self.to_jack,
            self.pos.line,
            self.pos.column
        )
