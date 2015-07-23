OFFSET = 0
RANGE = 1

def str_to_color(str):
    """ Return a twister color (1 - 126) for a given string """

    fword = str.split(' ', 1)[0]
    color = hash(fword) % 126

    return 1 + ((OFFSET + color * RANGE) % 125)

