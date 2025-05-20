import math
from dataclasses import dataclass

from blender3d_intergration.trajectories_api.models import Coordinates


@dataclass(frozen=True)
class LinearTrajectoryMotionInitialParameters:
    start_point: Coordinates
    end_point: Coordinates
    x_velocity_m_s: float
    y_velocity_m_s: float
    z_velocity_m_s: float


class LinearTrajectoryMotionParameters:
    __initial_parameters: LinearTrajectoryMotionInitialParameters

    def __init__(self, initial_parameters: LinearTrajectoryMotionInitialParameters):
        self.__initial_parameters = initial_parameters
        self.__time = self.__calculate_time(self.__initial_parameters)

    def get_time(self):
        return self.__time

    @staticmethod
    def __calculate_time(initial_parameters: LinearTrajectoryMotionInitialParameters) -> float:
        """
        Calculates end frame by calculating time required to traverse
        from start point to end point at given velocity magnitude calculated by vector composing
         \b
        end_frame = fps (frames per second in animation) x time[s]
         \b
        road = distance between end point and start point
         \b
        time = road / total_velocity_m_s
        """
        x_road = math.pow(initial_parameters.end_point.x - initial_parameters.start_point.x, 2)
        y_road = math.pow(initial_parameters.end_point.y - initial_parameters.start_point.y, 2)
        z_road = math.pow(initial_parameters.end_point.z - initial_parameters.start_point.z, 2)
        road_magnitude = math.sqrt(x_road + y_road + z_road)
        velocity_magnitude = math.sqrt(math.pow(initial_parameters.x_velocity_m_s, 2) +
                                       math.pow(initial_parameters.y_velocity_m_s, 2) +
                                       math.pow(initial_parameters.z_velocity_m_s, 2))

        return road_magnitude / velocity_magnitude