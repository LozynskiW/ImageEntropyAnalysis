import colorsys
from dataclasses import dataclass
from enum import Enum, StrEnum


class PlotFontSize(Enum):
    SMALL = (12, 16, 20)
    MEDIUM = (20, 24, 28)
    BIG = (28, 32, 36)

    def __init__(self, small_font, mid_font, big_font):
        self.small_font = small_font
        self.mid_font = mid_font
        self.big_font = big_font


# https://matplotlib.org/stable/users/explain/colors/colors.html#colors-def
class PlotColor(StrEnum):
    BLUE = 'b'
    GREEN = 'g'
    RED = 'r'
    CYAN = 'c'
    YELLOW = 'y'
    MAGENTA = 'm'
    BLACK = 'k'
    WHITE = 'w'
    VIOLET = "violet"
    BROWN = 'brown'
    SALMON = 'salmon'
    TEAL = 'teal'


class ViridisColors:
    class _ViridisColorsEnum(Enum):
        _MAGENTA = '#AD2E88'
        _DARK_PURPLE = '#225EA8'
        _PURPLE = '#4E2A84'
        _LIGHT_PURPLE = '#7F3C85'
        _BLUE = '#440154'
        _LIGHT_BLUE = '#41B6C4'
        _CYAN = '#35B779'
        _GREEN = '#21908C'
        _LIGHT_GREEN = '#7AD151'
        _LIGHT_YELLOW = '#FDC948'
        _YELLOW = '#FDE725'
        _ORANGE = '#FD8D3C'

        @classmethod
        def all_values(cls):
            return list(map(lambda c: c.value, cls))

    _index = 0
    _all_colors = _ViridisColorsEnum.all_values()

    @staticmethod
    def next_color():
        color = ViridisColors._all_colors[ViridisColors._index]

        if len(ViridisColors._all_colors) - 1 > ViridisColors._index:
            ViridisColors._index += 1
        else:
            ViridisColors._index = 0

        return color

    @staticmethod
    def get_lighter_version():
        factor=0.3
        hex_color = ViridisColors._all_colors[ViridisColors._index]
        r, g, b = int(hex_color[1:3], 16) / 255.0, int(hex_color[3:5], 16) / 255.0, int(hex_color[5:7], 16) / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + factor)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'


class PlotMarker(StrEnum):
    POINT = '.'
    CIRCLE = 'o'
    TRIANGLE_UP = '^'
    SQUARE = 's'
    PENTAGON = 'p'
    STAR = '*'
    HEXAGON1 = 'h'
    HEXAGON2 = 'H'
    PLUS = '+'
    X = 'x'
    DIAMOND = 'D'
    THIN_DIAMOND = 'd'


@dataclass
class FigureOptions:
    x_axis_label: str = ""
    y_axis_label: str = ""
    z_axis_label: str = ""
    title: str = ""
    font_size: PlotFontSize = PlotFontSize.MEDIUM


@dataclass
class PlotOptions:
    label: str
    x: list
    y: list
    z: list = None
    color: PlotColor = PlotColor.BLUE
    marker: PlotMarker = PlotMarker.CIRCLE


@dataclass
class PlotOptionsWithOYErrors:
    plot_options: PlotOptions
    y_errors: list
    x_errors: list
    errors_color: str
