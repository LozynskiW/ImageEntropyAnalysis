from abc import abstractmethod, ABC

from blender3d_intergration.object_trajectory_calculation.models import Trajectory, \
    Coordinates, CircularTrajectoryMotionParameters, CircularTrajectoryMotionInitialParameters, FramesPerSecond


class BasicBlenderTrajectoryCalculator:
    trajectory = []

    def get_trajectory(self):
        return self.trajectory

    @abstractmethod
    def set_path_parameters(self):
        raise NotImplementedError

    @abstractmethod
    def set_start_coordinates(self, start_x: int, start_y: int, start_z: int):
        raise NotImplementedError

    @abstractmethod
    def set_fps(self, fps: int):
        raise NotImplementedError

    @abstractmethod
    def get_trajectory_as_blender_script(self):
        raise NotImplementedError

    @abstractmethod
    def calculate_trajectory(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __calculate_coordinates(self, frame: int) -> Coordinates:
        raise NotImplementedError

    @abstractmethod
    def plot(self):
        raise NotImplementedError


class CircleTrajectory(BasicBlenderTrajectoryCalculator, ABC):
    _trajectory: Trajectory
    _initial_motion_parameters: CircularTrajectoryMotionInitialParameters
    _motion_parameters: CircularTrajectoryMotionParameters
    _fps: FramesPerSecond

    def __init__(self, initial_motion_parameters: CircularTrajectoryMotionInitialParameters, fps: FramesPerSecond):
        self._initial_motion_parameters = initial_motion_parameters
        self._motion_parameters = CircularTrajectoryMotionParameters(self._initial_motion_parameters)
        self._fps = fps
        self._trajectory = Trajectory()

    def get_initial_motion_parameters(self) -> CircularTrajectoryMotionInitialParameters:
        return self._initial_motion_parameters

    def get_motion_parameters(self) -> CircularTrajectoryMotionParameters:
        return self._motion_parameters

    def get_fps(self):
        return self._fps
