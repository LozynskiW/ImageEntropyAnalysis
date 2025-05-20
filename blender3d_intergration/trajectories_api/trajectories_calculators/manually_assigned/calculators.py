from abc import ABC

from blender3d_intergration.trajectories_api.models import CoordinatesInTime
from blender3d_intergration.trajectories_api.trajectories_calculators.manually_assigned.definitions import \
    ManuallyAssignedTrajectory


class ManuallyAssignedCoordinatesTrajectory(ManuallyAssignedTrajectory, ABC):

    def calculate_trajectory(self) -> None:
        pass

    def _calculate_end_frame(self) -> int:
        return self.get_trajectory().get_last_frame()

    def _calculate_coordinates(self, frame: int) -> CoordinatesInTime:
        pass
