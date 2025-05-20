from abc import ABC

from blender3d_intergration.trajectories_api.trajectories_calculators.linear.definitions import LinearTrajectory
from blender3d_intergration.trajectories_api.models import Coordinates


class SimpleLinearTrajectory(LinearTrajectory, ABC):
    """
    Calculates linear trajectory in 2D - either x or y or z from initial parameters must be constant
    - same for start and end point
    """

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
        return (self.get_initial_motion_parameters().start_point.x +
                self.get_initial_motion_parameters().x_velocity_m_s * time)

    def _calculate_y(self, time: float):
        return (self.get_initial_motion_parameters().start_point.y +
                self.get_initial_motion_parameters().y_velocity_m_s * time)

    def _calculate_z(self, time: float):
        return (self.get_initial_motion_parameters().start_point.z +
                self.get_initial_motion_parameters().z_velocity_m_s * time)