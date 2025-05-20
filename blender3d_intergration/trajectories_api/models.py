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


@dataclass(frozen=True, init=True)
class CoordinatesInTime:
    coordinates: Coordinates
    frame: int
    time_s: float


class Trajectory:
    __coordinates_in_time: list[CoordinatesInTime]

    def __init__(self, coordinates_in_time: list[CoordinatesInTime] | None = None):
        if coordinates_in_time is None:
            self.__coordinates_in_time = []
        else:
            self.__coordinates_in_time = coordinates_in_time

    def add_coordinates(self, coordinates: CoordinatesInTime):
        self.__coordinates_in_time.append(coordinates)

    def clear_coordinates(self) -> None:
        self.__coordinates_in_time.clear()

    def get_coordinates(self) -> list[CoordinatesInTime]:
        return deepcopy(self.__coordinates_in_time)

    def get_time_for_coordinates(self) -> list:
        return list(map(lambda c: c.time_s, self.__coordinates_in_time))

    def get_x_positions(self) -> list:
        return list(map(lambda c: c.x, self.__coordinates_in_time))

    def get_y_positions(self) -> list:
        return list(map(lambda c: c.y, self.__coordinates_in_time))

    def get_z_positions(self) -> list:
        return list(map(lambda c: c.z, self.__coordinates_in_time))

    def get_last_frame(self):
        return self.__coordinates_in_time[-1].frame
