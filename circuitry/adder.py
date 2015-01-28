from gates import xor

MAX_BITS = 8
range_bits = lambda: list(range(MAX_BITS))[::-1]


def half_adder(a, b):
    """
    >>> half_adder(0, 0)
    (0, 0)
    >>> half_adder(1, 0)
    (0, 1)
    >>> half_adder(0, 1)
    (0, 1)
    >>> half_adder(1, 1)
    (1, 0)


    (carry, sum)
    """
    return int(a and b), xor(a, b)


def full_adder(a, b, cin):
    either, a_b_xor = half_adder(a, b)

    cout = (a_b_xor and cin) or either

    return xor(a_b_xor, cin), int(cout)


def adder(a, b):
    def internal():
        carry = 0
        for i in range_bits():
            bit, carry = full_adder(a[i], b[i], carry)

            yield bit

    return list(internal())[::-1]


def split(a):
    a = int(a)
    return [
        int(bit)
        for bit in bin(a)[2:].rjust(MAX_BITS, '0')
    ]


def rejoin(a):
    return sum(
        a[(MAX_BITS-1)-i] * (2 ** i)
        for i in range_bits()
    )


def main():
    import sys

    res = adder(split(sys.argv[1]), split(sys.argv[2]))

    print(rejoin(list(res)))

if __name__ == '__main__':
    main()
