def k_to_int(string: str) -> int:
    string = string.lower()

    a = 1

    for i in string:
        if i == 'k' or i == 'к':
            a *= 1000

    a *= int(string.replace('k', '').replace('к', ''))

    return a


def ranks(x: int) -> str:
    return '{:,}'.format(x)
