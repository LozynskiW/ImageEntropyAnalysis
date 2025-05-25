from abc import ABC

from blender3d_intergration.trajectories_api.definitions import TrajectoryCalculator
from blender3d_intergration.trajectories_api.models import FramesPerSecond, Trajectory
from blender3d_intergration.trajectories_api.trajectories_calculators.circular.models import \
    CircularTrajectoryMotionInitialParameters, CircularTrajectoryMotionParameters


class CircleTrajectory(TrajectoryCalculator, ABC):
    _initial_motion_parameters: CircularTrajectoryMotionInitialParameters
    _motion_parameters: CircularTrajectoryMotionParameters

    def __init__(self, initial_motion_parameters: CircularTrajectoryMotionInitialParameters, fps: FramesPerSecond):
        self._initial_motion_parameters = initial_motion_parameters
        self._motion_parameters = CircularTrajectoryMotionParameters(self._initial_motion_parameters)
        self._fps = fps
        self._trajectory = Trajectory()

    def get_initial_motion_parameters(self) -> CircularTrajectoryMotionInitialParameters:
        return self._initial_motion_parameters

    def get_motion_parameters(self) -> CircularTrajectoryMotionParameters:
        return self._motion_parameters

