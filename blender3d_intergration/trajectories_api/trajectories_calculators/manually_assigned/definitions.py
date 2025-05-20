from abc import ABC

from blender3d_intergration.trajectories_api.definitions import TrajectoryCalculator
from blender3d_intergration.trajectories_api.models import Trajectory, FramesPerSecond, CoordinatesInTime


class ManuallyAssignedTrajectory(TrajectoryCalculator, ABC):

    def __init__(self, coordinates_in_time: list[CoordinatesInTime], fps: FramesPerSecond):
        self._fps = fps
        self._trajectory = Trajectory(coordinates_in_time)
