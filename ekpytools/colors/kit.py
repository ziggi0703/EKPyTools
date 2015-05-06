__author__ = 'Markus Prim'

from color_converters import rgb_to_hex_rep

green = rgb_to_hex_rep(0, 150, 130)
blue = rgb_to_hex_rep(70, 100, 170)
pea_green = rgb_to_hex_rep(140, 182, 60)
yellow = rgb_to_hex_rep(252, 229, 0)
orange = rgb_to_hex_rep(223, 155, 27)
brown = rgb_to_hex_rep(167, 130, 46)
red = rgb_to_hex_rep(162, 34, 35)
purple = rgb_to_hex_rep(163, 16, 124)
cyan_blue = rgb_to_hex_rep(35, 161, 224)


def get_palette(n_colors=5):
    """
    Load the kit color palette

    :param n_colors: number of different colors int hte palette
    :type n_colors: int

    :return: kit standard colors
    :rtype: list
    """
    colors = [green, pea_green, blue, cyan_blue, purple, brown, red, orange, yellow]

    if n_colors > len(colors):
        print 'Only {} different colors in list. All are returned.'
        return colors

    return colors[n_colors:]