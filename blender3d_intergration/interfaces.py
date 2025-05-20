from abc import abstractmethod, ABC

from matplotlib import pyplot as plt

from blender3d_intergration.trajectories_api.models import Trajectory, \
    Coordinates, CircularTrajectoryMotionParameters, CircularTrajectoryMotionInitialParameters, FramesPerSecond, \
    LinearTrajectoryMotionInitialParameters, LinearTrajectoryMotionParameters


class TrajectoryCalculator:
    _trajectory: Trajectory
    _fps: FramesPerSecond

    def calculate_trajectory(self) -> None:
        self._trajectory.clear_coordinates()

        end_frame = self._calculate_end_frame()

        for frame in range(0, end_frame + 1):
            coordinates_for_frame = self._calculate_coordinates(frame)
            self._trajectory.add_coordinates(coordinates_for_frame)

    def plot(self):
        x = self._trajectory.get_x_positions()
        y = self._trajectory.get_y_positions()
        z = self._trajectory.get_z_positions()

        ax = plt.figure().add_subplot(projection='3d')
        ax.scatter(x, y, z)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.grid()
        plt.show()

    def get_trajectory(self) -> Trajectory:
        return self._trajectory

    def get_fps(self):
        return self._fps

    @abstractmethod
    def _calculate_end_frame(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _calculate_coordinates(self, frame: int) -> Coordinates:
        raise NotImplementedError


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
