from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum


class FramesPerSecond(IntEnum):
    FPS_24 = 24,
    FPS_30 = 30


@dataclass(frozen=True, init=True)
class Coordinates:
    x: float
    y: float
    z: float
    frame: int
    time_s: float


class Trajectory:
    __coordinates: list[Coordinates]

    def __init__(self):
        self.__coordinates = []

    def add_coordinates(self, coordinates: Coordinates):
        self.__coordinates.append(coordinates)

    def clear_coordinates(self) -> None:
        self.__coordinates.clear()

    def get_coordinates(self) -> list[Coordinates]:
        return deepcopy(self.__coordinates)

    def get_time_for_coordinates(self) -> list:
        return list(map(lambda c: c.time_s, self.__coordinates))

    def get_x_positions(self) -> list:
        return list(map(lambda c: c.x, self.__coordinates))

    def get_y_positions(self) -> list:
        return list(map(lambda c: c.y, self.__coordinates))

    def get_z_positions(self) -> list:
        return list(map(lambda c: c.z, self.__coordinates))

    def get_last_frame(self):
        return self.__coordinates[-1].frame
