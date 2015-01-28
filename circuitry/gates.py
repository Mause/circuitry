import doctest


def xor(a, b):
    """
    exclusive or; a or b, but not both

    >>> xor(1, 0)
    1
    >>> xor(0, 1)
    1
    >>> xor(1, 1)
    0
    >>> xor(0, 0)
    0
    """
    return int((a or b) and not (a and b))


def _and(a, b):
    return int(a and b)


def _or(a, b):
    return int(a or b)


def _not(a):
    return int(not a)


if __name__ == '__main__':
    doctest.testmod()
