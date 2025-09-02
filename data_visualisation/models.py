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
    BLUE = "b"
    GREEN = 'g'
    RED = 'r'
    CYAN = 'c'
    YELLOW = 'y'
    MAGENTA = 'm'
    BLACK = 'b'
    WHITE = 'w'
    VIOLET = "violet"


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
