from abc import abstractmethod

from matplotlib import pyplot as plt

from blender3d_intergration.trajectories_api.models import Trajectory, \
    CoordinatesInTime, FramesPerSecond


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
    def _calculate_coordinates(self, frame: int) -> CoordinatesInTime:
        raise NotImplementedError
