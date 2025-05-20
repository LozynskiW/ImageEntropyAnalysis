import math
from dataclasses import dataclass

import numpy as np

from blender3d_intergration.trajectories_api.models import Coordinates


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
