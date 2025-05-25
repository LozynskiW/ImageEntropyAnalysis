from abc import ABC

import numpy as np

from blender3d_intergration.trajectories_api.models import CoordinatesInTime, Coordinates
from blender3d_intergration.trajectories_api.trajectories_calculators.circular.definitions import CircleTrajectory


class SimpleCircleTrajectory(CircleTrajectory, ABC):

    def _calculate_end_frame(self) -> int:
        """
        end_frame = fps (frames per second in animation) x time[s]

        Returns
        -------
        end_frame as int
        """

        return int(self._motion_parameters.get_time() * self._fps)

    def _calculate_coordinates(self, frame: int) -> CoordinatesInTime:
        time = frame / self.get_fps()
        x = self._calculate_x(time)
        y = self._calculate_y(time)
        z = self._calculate_z(time)
        return CoordinatesInTime(Coordinates(x,y,z), frame, time)

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
