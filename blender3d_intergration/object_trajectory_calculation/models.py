from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum

import numpy as np


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


@dataclass(frozen=True)
class CircularTrajectoryMotionInitialParameters:
    trajectory_center_point: Coordinates
    linear_velocity_m_s: float
    angular_displacement_degrees: int
    radius_m: float


class CircularTrajectoryMotionParameters:
    __initial_parameters: CircularTrajectoryMotionInitialParameters
    __angular_displacement_radians: float
    __time: float
    __angular_frequency: float

    def __init__(self, initial_parameters: CircularTrajectoryMotionInitialParameters):
        self.__initial_parameters = initial_parameters
        self.__time = self.__calculate_time(self.__initial_parameters)
        self.__angular_frequency = self.__calculate_angular_frequency(
            initial_parameters.angular_displacement_degrees, self.__time)

    def get_time(self):
        return self.__time

    def get_angular_frequency(self):
        return self.__angular_frequency

    @staticmethod
    def __calculate_time(initial_parameters: CircularTrajectoryMotionInitialParameters) -> float:
        """
        Calculates end frame by calculating time required to cover given angular_displacement_radians at trajectory
        constrained by radius_m and linear_velocity_m_s
         \b
        end_frame = fps (frames per second in animation) x time[s]
         \b
        time = road / linear_velocity_m_s
         \b
        road = angle[rad] x radius[m] = radius x (( angular_displacement_degrees x PI ) / 180)
        """
        radius = initial_parameters.radius_m
        angular_displacement_radians = (initial_parameters.angular_displacement_degrees * np.pi) / 180
        road = angular_displacement_radians * radius

        return road / initial_parameters.linear_velocity_m_s

    @staticmethod
    def __calculate_angular_displacement_radians(angular_displacement_degrees: int) -> float:
        return (angular_displacement_degrees * np.pi) / 180

    @staticmethod
    def __calculate_angular_frequency(angular_displacement_degrees: float, time: float) -> float:
        angular_displacement_radians = (angular_displacement_degrees * np.pi) / 180
        return angular_displacement_radians / time
