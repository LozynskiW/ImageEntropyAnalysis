from dataclasses import dataclass


@dataclass
class PlotOptions:
    x_axis: str = ""
    y_axis: str = ""
    z_axis: str = ""
    color: str = ""
    symbol: str = ""


class PlotOptionsBuilder:
    def __init__(self):
        self._options = PlotOptions()

    def x_axis(self, x_axis):
        self._options.x_axis = x_axis
        return self

    def y_axis(self, y_axis):
        self._options.y_axis = y_axis
        return self

    def z_axis(self, z_axis):
        self._options.z_axis = z_axis
        return self

    def color(self, color):
        self._options.color = color
        return self

    def symbol(self, symbol):
        self._options.symbol = symbol
        return self

    def build(self):
        return self._options