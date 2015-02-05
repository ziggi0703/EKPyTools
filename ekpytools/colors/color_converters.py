__author__ = 'Markus Prim'


def rgb_to_hex_rep(r, g, b):
    color = str()
    color += "#"
    color += str(hex(r)[2:]).zfill(2)
    color += str(hex(g)[2:]).zfill(2)
    color += str(hex(b)[2:]).zfill(2)
    return color

