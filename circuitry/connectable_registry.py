class ConnectableRegistry():
    def __init__(self):
        self.registry = {}

    @classmethod
    def instance(cls):
        try:
            cls._instance
        except AttributeError:
            cls._instance = cls()

        return cls._instance

    @classmethod
    def register(cls, klass_to_register):
        inst = cls.instance()

        inst.registry[klass_to_register.ttype] = klass_to_register

        return klass_to_register
