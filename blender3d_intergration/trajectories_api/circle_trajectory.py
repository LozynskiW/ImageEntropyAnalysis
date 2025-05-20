from abc import ABC

import numpy as np

from blender3d_intergration.interfaces import CircleTrajectory
from blender3d_intergration.trajectories_api.models import Coordinates, \
    CircularTrajectoryMotionInitialParameters


class SimpleCircleTrajectory(CircleTrajectory, ABC):

    def _calculate_end_frame(self) -> int:
        """
        end_frame = fps (frames per second in animation) x time[s]

        Returns
        -------
        end_frame as int
        """

        return int(self._motion_parameters.get_time() * self._fps)

    def _calculate_coordinates(self, frame: int) -> Coordinates:
        time = frame / self.get_fps()
        x = self._calculate_x(time)
        y = self._calculate_y(time)
        z = self._calculate_z(time)
        return Coordinates(x, y, z, frame, time)

    def _calculate_x(self, time: float):
        radius = self.get_initial_motion_parameters().radius_m
        ang_freq = self.get_motion_parameters().get_angular_frequency()
        return radius * np.cos(ang_freq * time)

    def _calculate_y(self, time: float):
        radius = self.get_initial_motion_parameters().radius_m
        ang_freq = self.get_motion_parameters().get_angular_frequency()
        return radius * np.sin(ang_freq * time)

    def _calculate_z(self, time: float):
        return self.get_initial_motion_parameters().trajectory_center_point.z


class CircularMotionInitialParametersGenerator:

    @staticmethod
    def changing_radius(center_point: Coordinates,
                        linear_velocity_m_s: float,
                        angular_displacement_degrees: int,
                        radius_m_list: list[float]
                        ) -> list[CircularTrajectoryMotionInitialParameters]:
        generated_initial_params = []

        for radius in radius_m_list:
            generated_initial_params.append(
                CircularTrajectoryMotionInitialParameters(
                    trajectory_center_point=center_point,
                    linear_velocity_m_s=linear_velocity_m_s,
                    angular_displacement_degrees=angular_displacement_degrees,
                    radius_m=radius
                )
            )

        return generated_initial_params
