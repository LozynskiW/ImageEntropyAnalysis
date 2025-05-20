import math
from abc import ABC

from blender3d_intergration.interfaces import TrajectoryCalculator
from blender3d_intergration.trajectories_api.models import FramesPerSecond, Trajectory
from blender3d_intergration.trajectories_api.trajectories_calculators.linear.models import \
    LinearTrajectoryMotionInitialParameters, LinearTrajectoryMotionParameters


class LinearTrajectory(TrajectoryCalculator, ABC):
    _initial_motion_parameters: LinearTrajectoryMotionInitialParameters
    _motion_parameters: LinearTrajectoryMotionParameters

    def __init__(self,
                 initial_motion_parameters: LinearTrajectoryMotionInitialParameters,
                 fps: FramesPerSecond):
        self._initial_motion_parameters = initial_motion_parameters
        self._motion_parameters = LinearTrajectoryMotionParameters(self._initial_motion_parameters)
        self._fps = fps
        self._trajectory = Trajectory()

    def get_initial_motion_parameters(self) -> LinearTrajectoryMotionInitialParameters:
        return self._initial_motion_parameters

    def get_motion_parameters(self) -> LinearTrajectoryMotionParameters:
        return self._motion_parameters
